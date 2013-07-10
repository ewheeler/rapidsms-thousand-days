from cleaver.reports.web import CleaverWebUI
from cleaver.backend.db import SQLAlchemyBackend

# TODO specify cleaver backend URI in settings
application = CleaverWebUI(
    SQLAlchemyBackend('sqlite:///experiments/experiment.data')
)
