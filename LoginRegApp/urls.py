from django.urls import path

from . import views

urlpatterns = [

    # ********** paths that render page **********

    path('', views.index),
    path('user_dashboard', views.user_dashboard),



    # ***** paths that redirect to render page *****

    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

]
