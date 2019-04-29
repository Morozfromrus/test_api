from django.contrib import admin
from daterange_filter.filter import DateRangeFilter

from app_api import models


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


@admin.register(models.CreditOrganization)
class CreditOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
        'rotation_start_datetime',
        'rotation_end_datetime',
        'minimum_score',
        'maximum_score',
        'credit_organization',
        'create_datetime',
        'update_datetime',
    )
    fields = (
        'name',
        'type',
        'rotation_start_datetime',
        'rotation_end_datetime',
        'minimum_score',
        'maximum_score',
        'credit_organization',
    )
    readonly_fields = (
        'create_datetime',
        'update_datetime',
    )
    raw_id_fields = ('credit_organization',)
    search_fields = ('name',)
    list_filter = (
        'type',
        ('create_datetime', DateRangeFilter),
        ('update_datetime', DateRangeFilter),
    )


@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'second_name',
        'first_name',
        'middle_name',
        'birthday',
        'phone',
        'passport',
        'score',
        'partner',
        'create_datetime',
        'update_datetime',
    )
    fields = (
        'second_name',
        'first_name',
        'middle_name',
        'birthday',
        'phone',
        'passport',
        'score',
        'partner',
    )
    readonly_fields = (
        'create_datetime',
        'update_datetime',
    )
    raw_id_fields = ('partner',)
    search_fields = (
        'second_name',
        'first_name',
        'middle_name',
        'phone',
        'passport',
    )
    list_filter = (
        ('birthday', DateRangeFilter),
        ('create_datetime', DateRangeFilter),
        ('update_datetime', DateRangeFilter),
    )


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'customer_profile',
        'offer',
        'status',
        'create_datetime',
        'send_datetime',
    )
    raw_id_fields = (
        'customer_profile',
        'offer',
    )
    search_fields = (
        'offer__name',
        'customer_profile__second_name',
        'customer_profile__first_name',
        'customer_profile__middle_name',
        'customer_profile__phone',
        'customer_profile__passport',
    )
    list_filter = (
        'status',
        ('create_datetime', DateRangeFilter),
        ('send_datetime', DateRangeFilter),
    )

