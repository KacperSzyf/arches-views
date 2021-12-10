import json
from django.http.response import JsonResponse

from django.contrib.auth import get_user_model

def is_none(string):
    if string.strip(): 
        return string
    else:
        return None
    


def list_users(request):
    #Load the model 
    User = get_user_model()

    #Get all users 
    users = [dict(username = usr.username, fullName = is_none(f"{usr.first_name} {usr.last_name}"), email = is_none(usr.email), isStaff = usr.is_staff, isSuperUser = usr.is_superuser) for usr in User.objects.all()]

    #Create a response dict
    response = dict(users = users)

    return JsonResponse(response, json_dumps_params = {'indent' : 2})