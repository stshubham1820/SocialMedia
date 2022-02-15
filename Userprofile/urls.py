
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard),
    path('friends/',views.friends),
    path('invite/',views.invite),
    path('myprofile/',views.myprofile),
    path('removefriend/',views.removefriend),
    path('addfriend/',views.addfriend),
    path('sendfriend/',views.sendfriend),
    path('pending/',views.pending),
    path('alluser/',views.alluser),
    path('friendprofile/',views.friendprofile),
    path('mutualfriend/',views.mutualfriend),
    path('notfriend/',views.unknown),
    path('createpost/',views.createpost),
    path('editprofile/',views.editprofile),
    path('logout/',views.Logout),

]
