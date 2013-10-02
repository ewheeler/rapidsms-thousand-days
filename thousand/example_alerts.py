import alerts
from alerts.models import Notification

def demo_alert():
    yield alerts.Alert('intruder alert! intruder alert!')

def notify():
    print 'notify'
    for i in xrange(3):
        notif = Notification(alert_type='thousand.example_notifications.DemoAlertType')
        notif.uid = 'notif-%d' % i
        notif.text = 'This is alert %d' % i
        notif.url = 'http://thousand-days.lobos.biz'
        yield notif
