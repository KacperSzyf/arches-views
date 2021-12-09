
from django.http.response import JsonResponse

from ..models.resource import Resource
from ..models.graph import Graph

def dashboard_data(request):

    data_array = []

    for gr in Graph.objects.all():
        temp = {}
        temp['modelName'] = gr.name
        temp['totalResources'] = len(Resource.objects.filter(graph = gr))
        data_array.append(temp)

    return JsonResponse(data_array, safe=False)