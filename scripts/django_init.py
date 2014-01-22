"""
Script to run after syncdb to populate database 
I prefer this to fixtures
"""

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

Site.objects.create()
admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')