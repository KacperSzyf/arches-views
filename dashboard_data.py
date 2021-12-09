
from django.http.response import JsonResponse

from arches.app.models.system_settings import settings
from arches.app.models.resource import Resource
from arches.app.models.graph import Graph
from arches.app.models.tile import Tile

#isresource is True, resource = branch
#isresource is False, resource = model

def dashboard_data(request):
    model_array = []
    branches_array = []
    total_model_resources = 0

    resources = Resource.objects.exclude()
    graphs = Graph.objects.exclude(graphid = settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID)

    for gr in graphs.exclude(isresource = False):
        model = {}
        model['modelName'] = gr.name
        model['totalResources'] = len(resources.filter(graph = gr))
        total_model_resources+=model['totalResources']
        model_array.append(model)
    
    for gr in graphs.exclude(isresource = True):
        branch = {}
        branch['branchName'] = gr.name
        branches_array.append(branch)
    
    metaData = {'totalResources' : total_model_resources,
    'totalModels' : len(model_array),
    'totalBranches' : len(branches_array)}

    return JsonResponse(
        {
        'metaData' : metaData,
        'modelCounts': model_array,
        'branchCounts': branches_array  
        },
      json_dumps_params = {'indent' : 2}
      )