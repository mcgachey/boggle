from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls import include, url

urlpatterns = [
    url(r'^boggle/', include('boggle_app.urls')),
]
urlpatterns += staticfiles_urlpatterns()
