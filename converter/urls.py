from django.conf.urls import url

from .views import UploadView

urlpatterns = [
    url(r'^$', UploadView.as_view(), name='home'),

]
