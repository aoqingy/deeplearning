from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listDots/', views.listDots),
    path('sampleDot/', views.sampleDot),
    path('clearDots/', views.clearDots),
    path('trainDot/', views.trainDot),
]
