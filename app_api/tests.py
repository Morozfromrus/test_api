from django.test import TestCase
from rest_framework.test import APIClient

from app_api import models


class ApiTests(TestCase):
    fixtures = ['test_data']

    @staticmethod
    def test_customer_profile_view_from_partner():
        client = APIClient()
        client.login(username='partner_1', password='123')

        res = client.get('/customer-profile')
        assert res.status_code == 200
        assert len(res.data) == 2
        assert res.data[0]['first_name'] == 'client_5_1'
        assert res.data[1]['first_name'] == 'client_30_1'

        res = client.get('/customer-profile/1')
        assert res.status_code == 200
        assert res.data['first_name'] == 'client_5_1'

        res = client.get('/customer-profile/3')
        assert res.status_code == 404

        res = client.get('/customer-profile/1/send_request')
        assert res.status_code == 200
        assert len(res.data) == 3
        assert res.data[0]['name'] == 'offer_5_20_1'

        res = client.get('/request')
        assert res.status_code == 200
        assert len(res.data) == 0

        res = client.post('/customer-profile/1/send_request', {'offer_id': 1}, format='json')
        assert res.status_code == 201

        res = client.get('/request')
        assert res.status_code == 200
        assert len(res.data) == 1

    @staticmethod
    def test_customer_profile_view_from_credit_organization():
        client = APIClient()
        client.login(username='credit_organization_1', password='123')

        res = client.get('/customer-profile')
        assert res.status_code == 403

        res = client.get('/customer-profile/1')
        assert res.status_code == 403

        res = client.get('/customer-profile/1/send_request')
        assert res.status_code == 403

    @staticmethod
    def test_request_from_credit_organization():
        client = APIClient()
        client.login(username='partner_1', password='123')

        res = client.post('/customer-profile/1/send_request', {'offer_id': 1}, format='json')
        assert res.status_code == 201

        client = APIClient()
        client.login(username='credit_organization_1', password='123')

        res = client.get('/request')
        assert res.status_code == 200
        assert len(res.data) == 1

        res = client.get('/request/1')
        assert res.status_code == 200
        assert res.data['customer_profile']['first_name'] == 'client_5_1'
        assert res.data['offer']['name'] == 'offer_5_20_1'
        assert res.data['status'] == models.Request.STATUSES.new

        res = client.post('/request/1/change_status_request', {
            'status': models.Request.STATUSES.approved
        }, format='json')
        assert res.status_code == 200

        res = client.get('/request/1')
        assert res.status_code == 200
        assert res.data['status'] == models.Request.STATUSES.approved

        client = APIClient()
        client.login(username='credit_organization_2', password='123')

        res = client.get('/request')
        assert res.status_code == 200
        assert len(res.data) == 0

    @staticmethod
    def test_request_from_credit_partner():
        client = APIClient()
        client.login(username='partner_1', password='123')

        res = client.post('/customer-profile/1/send_request', {'offer_id': 1}, format='json')
        assert res.status_code == 201

        res = client.get('/request')
        assert res.status_code == 200
        assert len(res.data) == 1

        res = client.get('/request/1')
        assert res.status_code == 200

        res = client.post('/request/2/change_status_request', {
            'status': models.Request.STATUSES.approved
        }, format='json')
        assert res.status_code == 403

        res = client.get('/request/1')
        assert res.status_code == 200
        assert res.data['status'] == models.Request.STATUSES.new
