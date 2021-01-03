from django.urls import path
from . import views

app_name = 'eda'
urlpatterns = [
    path('bootstrap/', views.load_eda, name="eda"),
    path('', views.ready_eda, name="ready"),
]