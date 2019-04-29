from rest_framework import serializers

from app_api.models import Offer, CustomerProfile, Request


class OfferListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offer-detail', read_only=True)

    class Meta:
        model = Offer
        fields = (
            'url',
            'id',
            'name',
            'type',
            'credit_organization',
        )


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'id',
            'name',
            'type',
            'minimum_score',
            'maximum_score',
            'rotation_start_datetime',
            'rotation_end_datetime',
            'credit_organization',
        )


class CustomerProfileListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='customer-profile-detail', read_only=True)

    class Meta:
        model = CustomerProfile
        fields = (
            'url',
            'id',
            'second_name',
            'first_name',
            'middle_name',
            'birthday',
            'phone',
            'passport',
            'score',
        )


class CustomerProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = (
            'id',
            'second_name',
            'first_name',
            'middle_name',
            'birthday',
            'phone',
            'passport',
            'score',
            'create_datetime',
            'update_datetime',
        )


class SendRequestSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(
        source='id',
        style={'base_template': 'input.html', 'placeholder': "Offer ID"}
    )

    class Meta:
        model = Offer
        fields = (
            'offer_id',
        )


class RequestListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='request-detail', read_only=True)

    class Meta:
        model = Request
        depth = 1
        fields = (
            'url',
            'id',
            'create_datetime',
            'send_datetime',
            'status',
        )


class RequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        depth = 1
        fields = (
            'id',
            'create_datetime',
            'send_datetime',
            'status',
            'customer_profile',
            'offer',
        )


class ChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            'status',
        )
