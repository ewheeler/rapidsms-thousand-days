from cleaver.reports.web import CleaverWebUI
from cleaver.backend.db import SQLAlchemyBackend

application = CleaverWebUI(
    SQLAlchemyBackend('sqlite:///experiments/experiment.data')
)
