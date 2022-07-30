from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from.views import home,voicetotext,texttovoice,download,download1
app_name='converter'

urlpatterns=[
    path('',home,name='home'),
    path('vtotxt/',voicetotext,name='v2txt'),
    path('txttov/',texttovoice,name='txt2v'),
    path('download/',download,name='download'),
    path('download1/',download1,name='download1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)