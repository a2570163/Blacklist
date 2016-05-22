from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.forms import AddBlacklistFormByManual, AddBlacklistFormByCSV
from django.http import HttpResponseRedirect
from app.models import Blacklist
import csv
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
@login_required(login_url='/')
def editBlackList(request):
    blacklist = Blacklist.objects.all()
    return render(request,
                  'edit.html',
                  {
                      'add_blacklist_form_by_manual': AddBlacklistFormByManual,
                      'add_blacklist_form_by_CSV': AddBlacklistFormByCSV,
                      'blacklists': blacklist,
                      'blacklistcount': blacklist.count()
                  })


@login_required(login_url='/')
def editProcess(request):
    if request.method == 'POST':
        if 'manual' == request.POST['update_type']:
            addBlacklistFormByManual = AddBlacklistFormByManual(request.POST)
            if addBlacklistFormByManual.is_valid():
                email = addBlacklistFormByManual.cleaned_data['email']
                type = addBlacklistFormByManual.cleaned_data['type']
                user_id = addBlacklistFormByManual.cleaned_data['user_id']
                # print email, type, user_id
                try:
                    Blacklist.objects.get(email=email, user_id=user_id)
                except ObjectDoesNotExist:
                    # Object not exist
                    status = Blacklist.objects.create(email=email, user_id=user_id, type=type)
                    if not status:
                        # Command database not success
                        return HttpResponseRedirect('/edit/?message=' + str(u'Error write into the database!'))
                    else:
                        # Success
                        return HttpResponseRedirect('/edit/?message=' + str(u'Success'))
                else:
                    # Object exist
                    return HttpResponseRedirect('/edit/?message=' + str(u'Email duplicate'))
            else:
                # Form not valid
                return HttpResponseRedirect('/edit/?message=' + str(addBlacklistFormByManual.errors))
        elif 'csvfile' == request.POST['update_type']:
            addBlacklistFormByCSV = AddBlacklistFormByCSV(request.POST, request.FILES)
            if addBlacklistFormByCSV.is_valid():
                tempfile = request.FILES.get('csvfile')
                data = csv.DictReader(tempfile)
                user_id = addBlacklistFormByCSV.cleaned_data['user_id']
                repeated = 0
                imported = 0
                for line in data:
                    try:
                        Blacklist.objects.get(email=line['email'], user_id=user_id)
                    except ObjectDoesNotExist:
                        # Object not exist
                        # print line['email'].replace(' ', ''), addBlacklistFormByCSV.cleaned_data['user_id'], line['type'].replace(' ', '')
                        status = Blacklist.objects.create(email=line['email'].replace(' ', ''), user_id=user_id,
                                                          type=line['type'].replace(' ', ''))
                        if not status:
                            # Command database not success
                            return HttpResponseRedirect('/edit/?message=' + str(u'Error write into the database!'))
                        else:
                            # Success
                            imported += 1
                    else:
                        # Object exist
                        repeated += 1
                return HttpResponseRedirect('/edit/?imported=' + str(imported) + '&repeated=' + str(repeated))
            else:
                # Form not valid
                return HttpResponseRedirect('/edit/?message=' + str(addBlacklistFormByCSV.errors))
        else:
            pass

    return HttpResponseRedirect('/edit/')
