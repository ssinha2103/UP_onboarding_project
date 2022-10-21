from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
#router.register('items', ItemsView, 'items')

urlpatterns = [
    # Homepage
    path("", ApiHomepage),

    #General APIs
    path("register/", UserRegisterView.as_view(), name='register'),
    path("login/", AuthUserLoginView.as_view(), name='login'),
    path("logout/", api_logout, name='logout'),
    path("users/", UserListView.as_view(), name="users"),
    path("stores/", StoresView.as_view(), name="stores"),
    path("items/", ItemsView.as_view(), name="items"),
    path("placeorders/", PlaceOrderView.as_view(), name="placeorders"),
    path("seeorders/", SeeOrderView.as_view(), name="seeorders")
]

urlpatterns += router.urls
