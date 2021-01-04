from django.urls import path
from . import views

app_name = 'eda'
urlpatterns = [
    path('', views.load_eda, name="eda"),
    path('profile/', views.profile, name="profile"),
    path('letter/', views.letter, name="letter"),
    path('test/', views.ready_eda, name="ready"),
]