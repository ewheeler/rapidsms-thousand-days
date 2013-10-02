import datetime

from django.contrib.auth.models import User

from alerts.models import NotificationType


class DemoAlertType(NotificationType):
    # notification starts out at the first level, and can be
    # escalated to each subsequent level
    escalation_levels = ['district', 'region', 'moh']

    # which users can see the alert at each level
    def users_for_escalation_level(self, esc_level):
        if esc_level == 'district':
            # return all users with reporting_district = district
            return User.objects.all()
        elif esc_level == 'region':
            # return designated follow-up person at regional level
            return User.objects.all()
        elif esc_level == 'moh':
            # return all users with group 'moh'
            return User.objects.all()

    # how long the alert can be at the given level before it is
    # auto-escalated to the next level
    def auto_escalation_interval(self, esc_level):
        return datetime.timedelta(days=14)

    # return a human-readable name for each escalation level
    def escalation_level_name(self, esc_level):
        return {
            'region': 'regional team',
            'district': 'district team',
            'moh': 'ministry of health',
        }[esc_level]
