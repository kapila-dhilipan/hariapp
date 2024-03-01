import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_countries.fields import CountryField
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpRequest

from ipware import get_client_ip

User = get_user_model()

logger = logging.getLogger(__name__)
class TrackerManager(models.Manager):
    """
    Custom ``Tracker`` model manager that implements a method to create a new
    object instance from an HTTP request.
    """
    def create_from_request(self, request):
        """
        Given an ``HTTPRequest`` object and a generic content, it creates a
        ``Tracker`` object to store the data of that request.

        :param request: A Django ``HTTPRequest`` object.
        :return: A newly created ``Tracker`` instance.
        """
        # Sanity checks.
        assert isinstance(request, HttpRequest), \
            '`request` object is not an `HTTPRequest`'
        
        user = str(request.user)   
        
        try:
            if getattr(request.user_agent, 'is_mobile', False):
                device_type = "mobile"
            elif getattr(request.user_agent, 'is_tablet', False):
                device_type = "tablet"
            elif getattr(request.user_agent, 'is_pc', False):
                device_type = "pc"
            elif getattr(request.user_agent, 'is_bot', False):
                device_type = 'bot'
        except Exception as e:
            logger.warning('Error parsing user agent: %s', str(e))

        city = {}

        # Get the IP address and so the geographical info, if available.
        ip_address, _ = get_client_ip(request) or ''
        if not ip_address:
            logger.debug('Could not determine IP address for request %s', request)
        else:
            geo = GeoIP2()
            try:
                city = geo.city(ip_address) 
            except Exception as e:
                city = geo.city("72.14.207.99")
                logger.error('Unable to determine geolocation for address %s: %s', ip_address, str(e))

        tracker = self.model.objects.create(
            ip_address=ip_address,
            ip_country=city.get('country_code', '') or '',
            ip_region=city.get('region', '') or '',
            ip_city=city.get('city', '') or '',
            referrer=request.META.get('HTTP_REFERER', ''),
            device_type=device_type,
            device=getattr(request.user_agent.device, 'family', ''),
            browser=getattr(request.user_agent.browser, 'family', '')[:30],
            browser_version=getattr(request.user_agent.browser, 'version_string', ''),
            system=getattr(request.user_agent.os, 'family', ''),
            system_version=getattr(request.user_agent.os, 'version_string', ''),
            user=user
        )

        logger.info('Tracked click in %s %s.', user.username, Tracker.ip_address)
        
        return tracker

# Create your models here.
class Tracker(models.Model):
    """
        The tracker model for storing and maintaining the visitors record it's associated 
        with the content type framework so that we can associate this model with any other model(table)
    """
    DEVICE_TYPE = (
        ('pc', 'PC'),
        ('mobile', 'MOBILE'),
        ('tablet', 'TABLET'),
        ('bot', 'BOT'),
        ("unknown", "UNKNOWN")
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True, db_index=True)
    ip_country = CountryField(blank=True, null=True)
    ip_region = models.CharField(max_length=255, blank=True, null=True)
    ip_city = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    device_type = models.CharField(
        max_length=10,
        choices=DEVICE_TYPE,
        default="UNKNOWN"
    )
    device = models.CharField(max_length=30, blank=True, null=True)
    browser = models.CharField(max_length=30, blank=True, null=True)
    browser_version = models.CharField(max_length=30, blank=True, null=True)
    system = models.CharField(max_length=30, blank=True, null=True)
    system_version = models.CharField(max_length=30, blank=True, null=True)
    user = models.CharField(max_length=30, blank=True, null=True)

    objects = TrackerManager()

    
    def __str__(self):
        user_str = str(self.user) if self.user else 'Anonymous User'
        return f'Tracker - User: {user_str}, IP: {self.ip_address}'

    