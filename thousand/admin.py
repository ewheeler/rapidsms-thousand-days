from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin
from reversion_compare.helpers import patch_admin

from appointments.models import Appointment
from appointments.models import Milestone
from appointments.models import TimelineSubscription
from appointments.models import Timeline
from appointments.models import Notification

patch_admin(Appointment)
patch_admin(Milestone)
patch_admin(TimelineSubscription)
patch_admin(Timeline)
patch_admin(Notification)


from rapidsms.models import Connections
from rapidsms.models import Contacts

patch_admin(Connections)
patch_admin(Contacts)


from django.contrib.auth.models import User
from django.contrib.auth.models import Group

patch_admin(User)
patch_admin(Group)
