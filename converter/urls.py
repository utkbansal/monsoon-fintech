from django.conf.urls import url

from .views import UploadView, ResultView

urlpatterns = [
    url(r'^$', UploadView.as_view(), name='home'),
    url(r'^result/$', ResultView.as_view(), name='result')

]
