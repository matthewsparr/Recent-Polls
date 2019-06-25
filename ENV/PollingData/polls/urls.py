from django.conf.urls import url
from . import views
app_name = 'polls'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    # ex: /polls/New-York/
    url(r'^(?P<category>[\w\-]+)/$', views.index, name='index'),
    # ex: /polls/New-York/12/results/
    url(r'^(?P<category>[\w\-]+)/(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
]