#!/usr/bin/env python
from django.conf import settings
from django.contrib.sites.models import Site

class SiteConf(object):

    def setup_site():
        site = Site.objects.get(domain=settings.DOMAIN)
        if not site:
            site = Site(domain=settings.DOMAIN, name=settings.SITE_NAME)
            site.save()
        settings.SITE_ID = site.id


if __name__ = 'main':
    pass