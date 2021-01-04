from django.contrib import admin
from .models import Dataframe, Graph_plot, Visitor

# Register your models here.
admin.site.register(Dataframe)
admin.site.register(Graph_plot)
admin.site.register(Visitor)