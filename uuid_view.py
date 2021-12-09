
from django.http.response import HttpResponse, JsonResponse

from arches.app.models.resource import Resource
from arches.app.utils.betterJSONSerializer import JSONSerializer

def uuid_view(request, input):
    resource  = Resource.objects.get(resourceinstanceid = input)
    print(resource)
    resource.load_tiles()
    print(resource.tiles)
    resource_json = JSONSerializer().serializeToPython(resource)

    return JsonResponse(resource_json, json_dumps_params = {'indent' : 2})