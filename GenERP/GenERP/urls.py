from django_otp.admin import OTPAdminSite

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# from profiles.views.account_data_views import account_data
# from settings.views.login_activity_views import LoginActivityView

# admin.site.__class__ = OTPAdminSite

# Enforce 2FA only in production.
'''
if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite
'''
admin.site.site_header = 'GenERP Portal'
admin.site.site_title = 'GenERP Platform'
admin.site.index_title = 'GenERP Platform'
admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path("hrms/",include("hrms.urls")),
    # path("auth/", include('admin_soft.urls')),
    
]


#  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)