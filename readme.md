### dashboard_data view
at the top of the `urls.py` document import the view eg.: `from .views.dashboard_data import dashboard_data`
add `path('dashboard_data/', dashboard_data, name='dashboard_data')` to `urls.py` in `urlpatterns` array


### uuid_view view
at the top of the `urls.py` document import the view eg.: `from .views.uuid_view import uuid_view`
add `path('uuid_view/<uuid:input>', uuid_view, name='uuid_view')` to `urls.py` in `urlpatterns` array
