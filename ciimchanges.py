#Imports
import math
from datetime import datetime
from time import time

from django.views.generic import View
from django.http import JsonResponse

from arches.app.models.system_settings import settings
from arches.app.utils.betterJSONSerializer import JSONSerializer

from arches.app.models.resource import Resource
from arches.app.models.models import LatestResourceEdit

class ChangesView(View):

    def get(self, request):
        #Timer start
        start_time = time()

        #Functions
        def get_data(from_date, to_date, per_page, page):
            '''
            Get all edited resources from selected page

            Returns:
            :tuple: Where [0] contains all ID's, [1] total of all ID's, [2] number of pages
            '''
            #Get all edits within time range
            edits = LatestResourceEdit.objects.filter(timestamp__range=(from_date, to_date)).order_by('timestamp')

            #Get all resrouce id's in edits
            resource_ids = [edit.resourceinstanceid for edit in edits]
            total_resources = len(resource_ids)
            #Paginate results
            no_pages = math.ceil(total_resources/per_page)
            resourceinstanceids = resource_ids[(page-1)*per_page:page*per_page]

            return (resourceinstanceids, total_resources, no_pages)

        def download_data(resourceinstanceids):
            '''
            Get all data as json
            '''
            #Remove settings changes
            if settings.SYSTEM_SETTINGS_RESOURCE_ID in resourceinstanceids:
                resourceinstanceids.remove(settings.SYSTEM_SETTINGS_RESOURCE_ID)

            data = []
            
            for resourceid in resourceinstanceids:
                if Resource.objects.filter(pk=resourceid).exists():
                    resource = Resource.objects.get(pk=resourceid)
                    resource.load_tiles()

                    if not(len(resource.tiles) == 1 and not resource.tiles[0].data):
                        resource_json = JSONSerializer().serializeToPython(resource)
                        if resource_json['displaydescription'] == '<Description>': resource_json['displaydescription'] = None
                        if resource_json['map_popup'] == '<Name_Type>': resource_json['map_popup'] = None
                        if resource_json['displayname'] == '<NMRW_Name>' : resource_json['displayname'] = None
                        data.append(resource_json)
                else:
                    data.append({'resourceinstance_id':resourceid, 'tiles':None})


            return data            

        #Process input
        #Dates
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        from_date = datetime.strptime(from_date, '%d-%m-%YT%H:%M:%SZ')
        to_date = datetime.strptime(to_date, '%d-%m-%YT%H:%M:%SZ')

        #Pages
        per_page = int(request.GET.get('perPage'))
        page = int(request.GET.get('page'))

        #Data
        db_time_start = time()
        db_data = get_data(from_date, to_date, per_page, page)
        db_time_end = time()

        json_data_time_start = time()
        json_data = download_data(db_data[0])
        json_data_time_end = time()

        end_time = time()
        
        #Dictionaries

        time_elapsed = {
            'total' : end_time - start_time,
            'dbQuery': db_time_end - db_time_start,
            'dataDownload': json_data_time_end - json_data_time_start 
            }

        metadata = {
            'from': from_date,
            'to': to_date,
            'totalNumberOfResources': db_data[1],
            'perPage': per_page,
            'page': page,
            'numberOfPages': db_data[2],
            'timeElapsed': time_elapsed
        }

        response = {'metadata': metadata, 'results':json_data}


        return JsonResponse(response, json_dumps_params={'indent': 2})
