import pytest
from pdb import Pdb
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

#from UP_onboarding_system.point_of_sale.models import *
from point_of_sale.models import Items, Stores, Orders

client = APIClient()
User = get_user_model()


# Merchant Login & Registration Test Case
@pytest.mark.django_db
def test_merchant_registration():
    payload = {"username": "merchant", "email": "merchant@gmail.com", "password": "password@123",
               "profile.name": "Merchant_User", "profile.role": 1}
    response = client.post("/register/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_merchant_login(merchant_data):
    response = client.post("/login/", dict(username="merchant", password="password@123"))
    assert response.status_code == 200


# Stores Creation EndPoint Test Case
@pytest.mark.django_db
def test_store_creation_api_endpoint(merchant_data):
    # import pdb; pdb.set_trace()
    response = client.post("/login/", dict(username="merchant", password="password@123"))
    token = response.data['access']
    req_send = client.post("/stores/",
                           dict(name="WhiteField Outlet", address="WhiteField", lat=13, lng=13, merchant=merchant_data),
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201


# Items Creation Endpoint Test Case
@pytest.mark.django_db
def test_item_creation_api_endpoint(merchant_data):
    #import pdb; pdb.set_trace()
    response = client.post("/login/", dict(username="merchant", password="password@123"))
    token = response.data['access']
    store = Stores.objects.create(name="Mc Donald's WhiteField Outlet", address="WhiteField", lat=13, lng=13,
                                  merchant=merchant_data)
    req_send = client.post("/items/", dict(name="Veg Burger", price=160, description="With Aloo Tikki", stores=store.pk),
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201
    items_present = set(Items.objects.all().values_list('name', flat=True))
    assert "Veg Burger" in items_present


# consumer Login & Registration Test Case
@pytest.mark.django_db
def test_consumer_registration():
    payload = {"username": "consumer", "email": "consumer@gmail.com", "password": "password@123",
               "profile.name": "consumer_User", "profile.role": 2}
    response = client.post("/register/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_consumer_login(consumer_data):
    response = client.post("/login/", dict(username="consumer", password="password@123"))
    assert response.status_code == 200


# Test Place Order Endpoints
@pytest.mark.django_db
def test_place_order_api_endpoints(merchant_data, consumer_data):
    #import pdb; pdb.set_trace()
    response = client.post("/login/", dict(username="consumer", password="password@123"))
    token = response.data["access"]
    orders_before = set(Orders.objects.all().values_list('merchant', flat=True))
    store = Stores.objects.create(name="WhiteField Outlet", address="WhiteField", lat=13, lng=13,
                                  merchant=merchant_data)
    item = Items.objects.create(name="Dosa", price=120, description="Sambhar Dosa", stores=store)
    req_send = client.post("/placeorders/",
                           dict(user=consumer_data, merchant=merchant_data.pk, store=store.pk, items=item.pk),
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201
    orders_present = set(Orders.objects.all().values_list('merchant', flat=True))
    assert len(orders_present)>len(orders_before)
