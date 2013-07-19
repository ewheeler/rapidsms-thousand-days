from django.conf import settings

from cleaver.reports.web import CleaverWebUI
from cleaver.backend.db import SQLAlchemyBackend

application = CleaverWebUI(
    SQLAlchemyBackend(settings.CLEAVER_DATABASE)
)
