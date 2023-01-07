from . import views
from django.urls import path


urlpatterns = [
     path('create/', views.urlCreateView.as_view(), name="create"),
     path('createhistory/', views.urlCreateHistory.as_view(), name="createhistory"),
     path('history/',
         views.get_urls_history,
         name = 'urlshistory'),
     path('urlslist/',
         views.get_urls,
         name = 'urlslist'),
     path('deletedurls/',
         views.get_deleted_urls,
         name = 'deletedurls')
]
