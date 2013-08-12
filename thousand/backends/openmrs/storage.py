from __future__ import absolute_import, unicode_literals

import datetime

from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils.timezone import now

from healthcare.backends import comparisons
from healthcare.backends.base import HealthcareStorage
from .models import Patient, Provider, PatientID


__all__ = ['DjangoStorage']


class DjangoStorage(HealthcareStorage):

    _comparison_mapping = {
        comparisons.EQUAL: 'exact',
        comparisons.LIKE: 'contains',
        comparisons.IN: 'in',
        comparisons.LT: 'lt',
        comparisons.LTE: 'lte',
        comparisons.GT: 'gt',
        comparisons.GTE: 'gte',
    }


    def _patient_to_dict(self, patient):
        "Convert a Patient model to a dictionary."
        # Mapping of all fields
        # Might need additional translation of field names
        result = model_to_dict(patient)
        if hasattr(patient, 'created_date'):
            result['created_date'] = patient.created_date
        if hasattr(patient, 'updated_date'):
            result['updated_date'] = patient.updated_date
        # openmrs includes `gender`, so also add as `sex`
        if hasattr(patient, 'gender'):
            result['sex'] = patient.gender
        # openmrs models do not have `status`
        result['status'] = 'A'
        # rapidsms-nutrition expects `birth_date`
        if hasattr(patient, 'birthdate'):
            result['birth_date'] = patient.birthdate
        return result

    def _provider_to_dict(self, provider):
        "Convert a Provider model to a dictionary."
        # Mapping of all fields
        # Might need additional translation of field names
        result = model_to_dict(provider)
        result['created_date'] = provider.created_date
        result['updated_date'] = provider.updated_date
        return result

    def _lookup_to_q(self, lookup):
        if len(lookup) == 1:
            # for queries like client.patients.filter(sex__in=['M', 'F'])
            # `lookup` may be a one element list containing the expected tuple
            field, op, value = lookup[0]
        else:
            field, op, value = lookup
        # openmrs app calls it `gender`, so substitute if called as `sex`
        if field == "sex":
            field = "gender"
        lookup_type = self._comparison_mapping[op]
        params = {'{0}__{1}'.format(field, lookup_type): value}
        return Q(**params)

    def _get_patient_by_id(self, id):
        "Get patient by pk."
        try:
            patient = Patient.objects.using('patients').get(pk=id)
        except (ValueError, Patient.DoesNotExist):
            patient = None
        return patient

    def _get_patient_for_source(self, id, source):
        "Get patient by source_id, source_name pair."
        try:
            patient = PatientID.objects.select_related('patient').get(
                uid=id, source=source).patient
        except (ValueError, PatientID.DoesNotExist):
            patient = None
        return patient

    def get_patient(self, id, source=None):
        "Retrieve a patient record by ID."
        if source:
            patient = self._get_patient_for_source(id, source)
        else:
            patient = self._get_patient_by_id(id)
        return self._patient_to_dict(patient) if patient is not None else None

    def create_patient(self, data):
        "Create a patient record."
        # FIXME: Might need additional translation of field names
        try:
            patient = Patient.objects.using('patients').create(**data)
        except:
            # FIXME: Can we make this exception tighter?
            patient = None
        return self._patient_to_dict(patient) if patient is not None else None

    def update_patient(self, id, data):
        "Update a patient record by ID."
        # FIXME: Might need additional translation of field names
        # FIXME: Might need additional error handling
        try:
            data['updated_date'] = now()
            return Patient.objects.using('patients').filter(pk=id)\
                                                    .update(**data)
        except ValueError:
            return False

    def delete_patient(self, id):
        "Delete a patient record by ID."
        try:
            patient = Patient.objects.using('patients').filter(pk=id)
        except ValueError:
            return False
        else:
            if patient.exists():
                patient.delete()
                return True
            return False

    def filter_patients(self, *lookups):
        "Find patient records matching the given lookups."
        # Construct Q objects from lookups
        if lookups:
            q = reduce(operator.and_, map(self._lookup_to_q, lookups))
        else:
            q = Q()
        return map(self._patient_to_dict, Patient.objects.using('patients')
                   .filter(q))

    def link_patient(self, id, source_id, source_name):
        "Associated a source/id pair with this patient."
        try:
            patient_id, created = PatientID.objects.get_or_create(
                uid=source_id, source=source_name, defaults={'patient_id': id}
            )
        except ValueError:
            return False
        else:
            return created

    def unlink_patient(self, id, source_id, source_name):
        "Remove association of a source/id pair with this patient."
        try:
            patient_id = PatientID.objects.filter(
                uid=source_id, source=source_name, patient=id
            )
        except ValueError:
            return False
        else:
            if patient_id.exists():
                patient_id.delete()
                return True
            return False

    def get_provider(self, id):
        "Retrieve a provider record by ID."
        try:
            provider = Provider.objects.get(pk=id)
        except (ValueError, Provider.DoesNotExist):
            provider = None
        return self._provider_to_dict(provider) if provider is not None else None

    def create_provider(self, data):
        "Create a provider record."
        # FIXME: Might need additional translation of field names
        try:
            provider = Provider.objects.create(**data)
        except:
            # FIXME: Can we make this exception tighter?
            provider = None
        return self._provider_to_dict(provider) if provider is not None else None

    def update_provider(self, id, data):
        "Update a provider record by ID."
        # FIXME: Might need additional translation of field names
        # FIXME: Might need additional error handling
        try:
            data['updated_date'] = now()
            return Provider.objects.filter(pk=id).update(**data)
        except ValueError:
            return False

    def delete_provider(self, id):
        "Delete a provider record by ID."
        try:
            provider = Provider.objects.filter(pk=id)
        except ValueError:
            return False
        else:
            if provider.exists():
                provider.delete()
                return True
            return False

    def filter_providers(self, *lookups):
        "Find provider records matching the given lookups."
        # Construct Q objects from lookups
        if lookups:
            q = reduce(operator.and_, map(self._lookup_to_q, lookups))
        else:
            q = Q()
        return map(self._provider_to_dict, Provider.objects.filter(q))
