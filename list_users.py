import json
from django.http.response import JsonResponse

from django.contrib.auth import get_user_model

def list_users(request):
    #Load the model 
    User = get_user_model()

    #Get all users 
    users = [dict(username = usr.username, fullName = f"{usr.first_name} {usr.last_name}", email = usr.email, isStaff = usr.is_staff, isSuperUser = usr.is_superuser) for usr in User.objects.all()]

    #Create a response dict
    response = dict(users = users)

    return JsonResponse(response, json_dumps_params = {'indent' : 2})