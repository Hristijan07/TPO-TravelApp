from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('test/username=<slug:user>', views.test_user_trip, name='test'),
    path('test/user/id=<int:id>', views.get_user, name='get_user'),
    path('test/token', views.get_token, name='get_token'),

    path('add', views.add_items, name='add_items'),
    path('add/users', views.add_users, name='add_user'),
    path('add/interests', views.add_interests, name='add_interests'),
    path('add/company', views.add_company, name='add_company'),

    #destination
    path('dest', views.destination, name='destination'),
    path('dest/pk=<int:pk>', views.get_destination_by_id, name='get_destinations_by_id' ),
    path('dest/fk=<int:fk>', views.get_destination_by_trip_id, name='get_destination_by_trip_id'),

    #trips
    path('trip', views.trip, name='trip'),
    path('trip/<int:pk>', views.get_trip_by_id, name='get_trip_by_id'),

    #interests
    path('interests', views.interests, name='interests'),
    path('user/interests', views.user_interests, name='user_interests'),

    #company
    path('user/company', views.user_company, name='user_company'),

    #user
    path('user/info', views.user_info, name='user_info'),
    path('user/info/add', views.user_add, name='user_add'),

    #recommendation
<<<<<<< HEAD
    path('recommend/city=<slug:city>', views.get_recommendations, name='get_recommendations'),
=======
    path('recommend/destination_id=<int:destination_id>', views.get_recommendations, name='get_recommendations'),
>>>>>>> 85b83f186ebda63997a0c1fec6c7a34475271310
]