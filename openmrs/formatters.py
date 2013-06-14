from django.core.urlresolvers import reverse
from avocado.formatters import registry
from serrano.formatters import HTMLFormatter
from datetime import date


def process_age(dob, date_end):
    if not dob or not date_end:
        return "<em class='muted'>Unknown</em>"
    else:
        age = ((date_end - dob).total_seconds())/60/60/24/365.242
        age = round(age, 1)

        time = "years"
        if age < 1.0:
            age = ((date_end - dob).total_seconds())/60/60/24/30.4368
            age = round(age, 1)
            time = "months"
            if age < 1.0:
                age = ((date_end - dob).total_seconds())/60/60/24
                age = round(age, 1)
                time = "days"
                if age == 1.0:
                    time = "day"
            elif age == 1.0:
                time = "month"

        elif age == 1.0:
            time = "year"

        return age, time


class AgeFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        dob = values['birthdate']
        est = values['birthdate_estimated']

        if not dob:
            return "Current age not available"
        age, time = process_age(dob, date.today())

        if est:
            return "{0} {1} old <em class='muted'>(estimated)</em>".format(age, time)
        else:
            return "{0} {1} old".format(age, time)

    to_html.process_multiple = True

    def to_string(self, values, **context):
        dob = values['birthdate']
        est = values['birthdate_estimated']

        if not dob:
            return [{'value': None, 'time': None, 'est':None}]

        age, time = process_age(dob, date.today())

        if est:
            return [{'value':str(age), 'time':time, 'est': 'estimated'}]
        else:
            return [{'value':str(age), 'time':time, 'est':''}]

    to_string.process_multiple = True

    def to_boolean(self, values, **context):
        dob = values['birthdate']
        est = values['birthdate_estimated']

        if not dob:
            return [{'value': None, 'time': None, 'est':None}]

        age, time = process_age(dob, date.today())

        if est:
            return [{'value':age, 'time':time, 'est': True}]
        else:
            return [{'value':age, 'time':time, 'est': False}]

    to_boolean.process_multiple = True

    def to_number(self,values, **context):
        dob = values['birthdate']
        est = values['birthdate_estimated']

        if not dob:
            return [{'value': None, 'time': None, 'est':None}]

        age, time = process_age(dob, date.today())

        if est:
            return [{'age':age, 'time':time, 'est':est}]
        else:
            return [{'age':age, 'time':time, 'est':est}]

    to_number.process_multiple = True


class EncounterAgeFormatter(HTMLFormatter):

    def to_html(self, values, **context):
        dob = values['birthdate']
        est = values['birthdate_estimated']
        enc = values['encounter_datetime']

        if not enc or not enc.date:
            return ''
        enc_date = date(enc.year, enc.month, enc.day)

        age, time = process_age(dob, enc_date)

        if est:
            return "{0} {1} old <em class='muted'>(estimated)</em>".format(age, time)
        else:
            return "{0} {1} old".format(age, time)

    to_html.process_multiple = True


class GenderFormatter(HTMLFormatter):
    def to_html(self, value, **context):
        gender_map = {
            'M': 'Male',
            'F': 'Female',
        }
        if value in gender_map:
            return gender_map[value]
        return '<span class="muted">Unknown</span>'


class CbcPanelFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        test_names = ['hgb','wbc','rbc','platelets','mcv','hct','rdw','mchc','mch']

        html_str = ""
        for name in test_names:
            if values[name] != None:
                data_field = DataField.objects.get_by_natural_key('openmrs', 'labresult', name)
                html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped'>{0}</table>".format(html_str)
        return "<div class='muted'><h5>No Complete Blood Count Panel</h5></div>"

    to_html.process_multiple = True


class Chem7PanelFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        test_names = ['cr','bun','glu','na','k','cl','co2']

        html_str = ""
        for name in test_names:
            if values[name] != None:
                data_field = DataField.objects.get_by_natural_key('openmrs', 'labresult', name)
                html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped'>{0}</table>".format(html_str)
        return "<div class='muted'><h5>No Chem7 Panel</h5></div>"

    to_html.process_multiple = True


class MiscPanelFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        test_names = ['cd4','cd4_percent','cd8','sgpt','alc']

        html_str = ""
        for name in test_names:
            if values[name] != None:
                data_field = DataField.objects.get_by_natural_key('openmrs', 'labresult', name)
                html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped'>{0}</table>".format(html_str)
        return ""

    to_html.process_multiple = True


class SystemsFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        test_names = ['heent','chest','abdominal','cardiac','musculoskeletal', 'neurologic']

        html_str = ""
        for name in test_names:
            if values[name] != None:
                data_field = DataField.objects.get_by_natural_key('openmrs', 'systemsreview', name)
                if values[name] == 'ABNORMAL':
                    html_str += "<tr class=error><td>{0}</td><td class=text-error>{1}</td></tr>".format(data_field, values[name])
                else:
                    html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped'>{0}</table>".format(html_str)
        return ""

    to_html.process_multiple = True


class HIVDetailFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        test_names = ['plan','treat_adhere','stage_adult','stage_adult_last','stage_peds','cdc_category', 'taking_antiretrovirals', 'discordant_couple']

        html_str = ""
        for name in test_names:
            if values[name] != None:
                data_field = DataField.objects.get_by_natural_key('openmrs', 'hivdetails', name)
                html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped'>{0}</table>".format(html_str)
        return ""

    to_html.process_multiple = True


class TBDetailFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        test_names = ['treat_adhere','treat_plan','pro_adhere','pro_plan']
        html_str = ""
        for name in test_names:
            if values[name] != None and values[name] != 'NONE':
                data_field = DataField.objects.get_by_natural_key('openmrs', 'tbdetails', name)
                html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped'>{0}</table>".format(html_str)
        return ""

    to_html.process_multiple = True


class PCPDetailFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        test_names = ['plan','pro_adhere']
        html_str = ""
        for name in test_names:
            if values[name] != None and values[name] != 'NONE':
                data_field = DataField.objects.get_by_natural_key('openmrs', 'pcpdetails', name)
                html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped'>{0}</table>".format(html_str)
        return ""

    to_html.process_multiple = True


class MRNFormatter(HTMLFormatter):
    def to_html(self, value, **context):
        url = reverse('patient-detail', kwargs={'pk': value})
        return '<a href="{0}">MR{1}</a>'.format(url, str(value).zfill(8))


registry.register(AgeFormatter, 'Age')
registry.register(GenderFormatter, 'Gender')
registry.register(EncounterAgeFormatter, 'EncounterAge')
registry.register(CbcPanelFormatter, 'CbcPanel')
registry.register(Chem7PanelFormatter, 'Chem7')
registry.register(MiscPanelFormatter, 'MiscLab')
registry.register(SystemsFormatter, 'SystemsReview')
registry.register(HIVDetailFormatter, 'HIVDetail')
registry.register(TBDetailFormatter, 'TBDetail')
registry.register(PCPDetailFormatter, 'PCPDetail')
registry.register(MRNFormatter, 'MRN')
