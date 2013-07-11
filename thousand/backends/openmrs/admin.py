from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from .models import Patient
from .models import PatientID
from .models import Provider

class PatientAdmin(CompareVersionAdmin):
    pass

class PatientIDAdmin(CompareVersionAdmin):
    pass

class ProviderAdmin(CompareVersionAdmin):
    pass

admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientID, PatientIDAdmin)
admin.site.register(Provider, ProviderAdmin)
