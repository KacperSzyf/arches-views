from django.http.response import JsonResponse

from arches.app.models.system_settings import settings
from arches.app.models.resource import Resource
from arches.app.models.graph import Graph
from arches.app.models.models import Concept


#isresource is True, resource = branch
#isresource is False, resource = model

def dashboard_data(request):

    #varibles
    model_array = []
    total_model_resources = 0
    concepts = Concept.objects.all()

    #Get QuerySet of all Resources
    resources = Resource.objects.all()
    
    #Get QuerySet of all Graphs excluding the system_settings.py Graph
    graphs = Graph.objects.exclude(graphid = settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID)

    #Gather data for each model
    for gr in graphs.exclude(isresource = False):
        total_model_resources+=resources.filter(graph = gr).count()
        model_array.append(dict(name = gr.name, count = len(resources.filter(graph = gr))))
    
    #Gather data for each branch
    branches_array = [dict(name = gr.name) for gr in graphs.exclude(isresource = True)]

    #Get nodetypes
    nodetype_values = Concept.objects.values_list('nodetype', flat = True).distinct()
    
    #Gather concepts 
    concept_array = [dict(type = nodetype, count = concepts.filter(nodetype = nodetype).count()) for nodetype in nodetype_values]

    #Create metadata dictionary 
    metaData = {
        'totalResources' : total_model_resources,
        'totalModels' : len(model_array),
        'totalBranches' : len(branches_array)
        }

    #Create return dicitonary
    response = {
        'metaData' : metaData,
        'resourceModels': model_array,
        'branches': branches_array ,
        'referenceData' : concept_array
        }

    #return
    return JsonResponse( response, json_dumps_params = {'indent' : 2})