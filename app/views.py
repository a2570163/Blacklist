from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.forms import AddBlacklistFormByManual, AddBlacklistFormByCSV
from django.http import HttpResponseRedirect, JsonResponse
from app.models import Blacklist
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers


# Create your views here.
@login_required(login_url='/')
def editBlackList(request):
    """
    :param request: When the edit page has been loaded, this function will be called automatically
    :return: Render two forms('AddBlacklistFormByManual' and 'AddBlacklistFormByCSV') to the edit page
    """
    return render(request,
                  'edit.html',
                  {
                      'add_blacklist_form_by_manual': AddBlacklistFormByManual,
                      'add_blacklist_form_by_CSV': AddBlacklistFormByCSV,
                  })


@login_required(login_url='/')
def editProcess(request):
    """
    :param request: Requests from users, and it has been separated from two parts.
                        - 1. Request from form 'AddBlacklistFormByManual'
                        - 2. Request from form 'AddBlacklistFormByCSV'
    :return: The information after processing by different ways: Error or success, and event the error's reason
    """
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


@login_required(login_url='/')
def ajaxSearch(request):
    """
    :param request: Request from the ajax searching form, by using the searching input
    :return: Information after processing, in JSON format
    """
    content = {}
    if request.method == 'POST':
        print request.POST
        emaillist = serializers.serialize('json', Blacklist.objects.filter(email__istartswith=request.POST['email'],
                                                                           user_id=request.POST['user_id']))
        content['emaillist'] = emaillist
    else:
        content['emaillist'] = 'Error, method not allowed.'
    return JsonResponse(content)


@login_required(login_url='/')
def deleteDbByAjax(request):
    """
    :param request: Request from the Data Table, by clicking the beside 'delete' button.
                    This function using the AJAX too, to delete the selected objects from the database.
                    For do not refresh the whole page or the data table after deleting action.
    :return: Information after processing, in JSON format
    """
    content = {}
    if request.method == 'POST':
        print request.POST
        try:
            targetEmail = Blacklist.objects.get(email=request.POST['email'], user_id=request.POST['user_id'])
        except ObjectDoesNotExist:
            # Object not exist
            content['result'] = 'Delete failed.'
        else:
            # Object exists
            targetEmail.delete()
            content['result'] = 'Delete successful.'
    else:
        content['result'] = 'Error, method not allowed.'
    return JsonResponse(content)
