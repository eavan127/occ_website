# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from registration.models import UserInfo

admin.site.register(UserInfo)
