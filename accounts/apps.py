from django.apps import AppConfig
from watson import search


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        import accounts.signals
        Company = self.get_model("EmployerProfile")
        search.register(Company)
