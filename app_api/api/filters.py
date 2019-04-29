from django_filters import FilterSet
from django.contrib.auth.models import User


class CreditOrganizationFilter(FilterSet):
    model = User
    fields = ['credit_organization']

