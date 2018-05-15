import debug_toolbar
from django.urls import path, include
from django.conf import settings
from .base import urlpatterns

debugpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += debugpatterns
