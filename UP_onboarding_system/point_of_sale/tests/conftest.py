import pytest
from django.contrib.auth import get_user_model
from point_of_sale.models import Profile

User = get_user_model()


@pytest.fixture
def merchant_data():
    merchant = User.objects.create_user(username="merchant", email="merchant@gmail.com", password="password@123")
    profile = Profile.objects.create(user=merchant, name="Merchant_User", role=1)
    return profile


@pytest.fixture
def consumer_data():
    consumer = User.objects.create_user(username="consumer", email="consumer@gmail.com", password="password@123")
    profile = Profile.objects.create(user=consumer, name="consumer_User", role=2)
    return profile
