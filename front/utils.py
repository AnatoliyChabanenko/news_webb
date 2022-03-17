from django.db.models import Count

from .models import *





class DataMixin:
    paginate_by = 20

    def get_user_context(self, **kwargs):
        context = kwargs
        return context