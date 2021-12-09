
from django.http.response import JsonResponse

from arches.app.models.system_settings import settings
from arches.app.models.resource import Resource
from arches.app.models.graph import Graph
from arches.app.models.tile import Tile

#isresource is True, resource = branch
#isresource is False, resource = model

def dashboard_data(request):

    model_array = []
    total_model_resources = 0

    resources = Resource.objects.exclude()
    graphs = Graph.objects.exclude(graphid = settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID)

    for gr in graphs.exclude(isresource = False):
        total_model_resources+=len(resources.filter(graph = gr))
        model_array.append(dict(modelName = gr.name, totalResources = len(resources.filter(graph = gr))))
    
    branches_array = [dict(branchName = gr.name) for gr in graphs.exclude(isresource = True)]

    print(type(graphs))
    
    metaData = {'totalResources' : total_model_resources,
    'totalModels' : len(model_array),
    'totalBranches' : len(branches_array)}

    return JsonResponse(
        {
        'metaData' : metaData,
        'modelCounts': model_array,
        'branches': branches_array  
        },
      json_dumps_params = {'indent' : 2}
      )