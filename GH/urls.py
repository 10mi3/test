from hospital import urls as hospital_urls
from django.contrib import admin
from django.urls import path
urlpatterns = []
urlpatterns += hospital_urls.urlpatterns
from hospital.urls import urlpatterns as hospital_urlpatterns
# from notification.urls import urlpatterns as notification_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),

]

urlpatterns += hospital_urlpatterns