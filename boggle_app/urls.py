from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'solve$', views.solve, name='boggle_solve'),
    url(r'$', views.index, name='boggle_index'),
]
