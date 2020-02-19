from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('lecture/<int:lecture_id>', views.lecture, name='lecture'),    
    path('prof/<int:prof_id>', views.prof, name='prof'),
]