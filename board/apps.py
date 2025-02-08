from django.apps import AppConfig
from watson import search


class BoardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "board"

    def ready(self):
        JobListing = self.get_model("JobListing")
        search.register(JobListing)
