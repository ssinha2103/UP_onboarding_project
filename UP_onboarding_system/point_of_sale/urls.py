from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
# router.register('items', ItemsView, 'items')

urlpatterns = [
    # Homepage
    path("", ApiHomepage),

    # General APIs
    path("register/", UserRegisterView.as_view(), name='register'),
    path("login/", AuthUserLoginView.as_view(), name='login'),
    path("logout/", api_logout, name='logout'),
    path("change_password/", UserChangePasswordView.as_view(), name="change_password"),
    path("users/", UserListView.as_view(), name="users"),
    path("stores/", StoresView.as_view(), name="stores"),
    path("items/", ItemsView.as_view(), name="items"),
    path("place_orders/", PlaceOrderView.as_view(), name="place_orders"),
    path("see_orders/", SeeOrderView.as_view(), name="see_orders")
]

urlpatterns += router.urls
