from django.utils import timezone
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, views, status
from rest_framework.exceptions import ValidationError, bad_request, PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

from app_api.apps import AppApiConfig
from app_api import models
from app_api.api.permissions import CustomDjangoModelPermissions, OwnerPermissions
from app_api.api import serializers


class CustomerProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions, OwnerPermissions,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = (
        'second_name',
        'first_name',
        'middle_name',
    )
    filterset_fields = (
        'birthday',
        'phone',
        'passport',
        'score',
        'partner',
    )

    @action(detail=True, methods=['post', 'get'], name='Send request to credit organization')
    def send_request(self, request, pk=None):
        if not request.user.has_perm('{}.send_request'.format(AppApiConfig.name)):
            raise PermissionDenied

        profile = self.get_object()

        # Show available offers
        if request.method == 'GET':
            serializer = serializers.OfferDetailSerializer(models.Offer.objects.filter(
                rotation_start_datetime__lte=timezone.now(),
                rotation_end_datetime__gte=timezone.now(),
                minimum_score__lte=profile.score,
                maximum_score__gte=profile.score,
            ), many=True)
            return Response(serializer.data)

        offer_id = request.data.get('offer_id')

        # Check offer availability
        if offer_id is None or not models.Offer.objects.filter(
            id=offer_id,
            rotation_start_datetime__lte=timezone.now(),
            rotation_end_datetime__gte=timezone.now(),
            minimum_score__lte=profile.score,
            maximum_score__gte=profile.score,
        ).exists():
            raise ValidationError

        # Create and send request
        models.Request.objects.create(
            create_datetime=timezone.now(),
            send_datetime=timezone.now(),
            customer_profile=profile,
            offer_id=offer_id
        )

        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        if not self.request.user.profile.partner:
            raise ValidationError('User is not partner')
        serializer.save(partner=self.request.user.profile.partner)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CustomerProfileListSerializer
        elif self.action == 'send_request':
            return serializers.SendRequestSerializer
        else:
            return serializers.CustomerProfileDetailSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.CustomerProfile.objects.all()
        if hasattr(self.request.user, "partner"):
            return models.CustomerProfile.objects.filter(partner=self.request.user.partner)
        else:
            return models.CustomerProfile.objects.none()


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions, OwnerPermissions,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = (
        'status',
        'customer_profile',
        'offer',
    )

    @action(detail=True, methods=['post', 'get'], name='Change status')
    def change_status_request(self, request, pk=None):
        if not request.user.has_perm('{}.change_status_request'.format(AppApiConfig.name)):
            raise PermissionDenied

        request_obj = self.get_object()

        if request.method == 'GET':
            return Response(serializers.RequestDetailSerializer(request_obj).data)

        _status = request.data.get('status')

        # Check status availability
        if _status not in models.Request.STATUSES:
            raise ValidationError

        # Change status
        request_obj.status = _status
        request_obj.save()
        return Response({'status': 'ok'})

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RequestListSerializer
        elif self.action == 'change_status_request':
            return serializers.ChangeStatusSerializer
        else:
            return serializers.RequestDetailSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Request.objects.all()
        elif hasattr(self.request.user, "credit_organization"):
            return models.Request.objects.filter(
                offer__in=self.request.user.credit_organization.offers.all()
                .select_related('offer', 'customer_profile')
            )
        elif hasattr(self.request.user, "partner"):
            return models.Request.objects.filter(
                customer_profile__in=self.request.user.partner.customer_profiles.all()
                .select_related('offer', 'customer_profile')
            )
        else:
            return models.Request.objects.none()
