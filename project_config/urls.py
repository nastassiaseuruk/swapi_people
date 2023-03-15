"""project_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from people import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.list_collections, name='colections-view'),
    path('collection/<uuid:collection_uuid>/', views.get_collection, name='colection-detail-view'),
    path('collection/<uuid:collection_uuid>/value_count', views.get_collection_value_count, name='colection-detail-view-value'),
    path('load_new_dataset/', views.load_collection, name='load-view'),
]
