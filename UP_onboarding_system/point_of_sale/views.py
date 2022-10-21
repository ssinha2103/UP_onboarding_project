import json
# Logging Stuff
# import logging
import structlog

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsMerchant, IsConsumer
from .serializers import *

from .tasks import create_an_order

# _logger = logging.getLogger(__name__)
# logger_name = str(_logger).upper()

_logger = structlog.get_logger(__name__)
logger_name = str(_logger).upper()


def return_role(user):
    p = Profile.objects.get(user=user)
    if p.role == 1:
        role = "Merchant"
    elif p.role == 2:
        role = "Customer"
    return role


@api_view(['GET'])
def ApiHomepage(request, format=None):
    _logger.info(event='Into Home Page', user=request.user.username, into=logger_name)
    return Response({
        # General API URI
        'Register': reverse_lazy('register', request=request, format=format),
        'Login': reverse_lazy('login', request=request, format=format),
        'Logout': reverse_lazy('logout', request=request, format=format),
        'Users': reverse_lazy('users', request=request, format=format),
        'Stores': reverse_lazy('stores', request=request, format=format),
        'Items': reverse_lazy('items', request=request, format=format),
        'Place orders': reverse_lazy('placeorders', request=request, format=format),
        'View orders': reverse_lazy('seeorders', request=request, format=format),
    })


# Create your views here.


@api_view(["GET"])
@permission_classes([AllowAny])
def api_logout(request):
    request.session.flush()
    _logger.warning(event='User Logged Out', user=request.user.username, into=logger_name)
    return Response(status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    _logger.info(event='New User Registration !', into='User Registration page')

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            print(json.dumps(request.data))
            serializer.save()
            status_code = status.HTTP_201_CREATED
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }
            # _logger.info(
            #     logger_name + ":- " + self.request.user.username + " ( With role :- " + return_role(
            #         user) + ') New User Registered '
            #                 'Successfully and LoggedIn'
            #                 ' !!!')
            _logger.info(event='New User Registration !', user=request.user.username, role=return_role(user),
                         message='User Registration completed')
            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    _logger.info(event='User Login !', into='User Login page')

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            pk = User.objects.get(username=serializer.data['username']).pk
            role = Profile.objects.get(user=pk).role
            print(role)
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                    'role': role
                }
            }
            # _logger.info(
            #     logger_name + ":- " + self.request.user.username + " (With role :- " + return_role(
            #         user) + ') User Logged In Successfully !!!')
            _logger.info(event='User Login !', user=request.user.username, role=return_role(user),
                         message='User Login completed')
            return Response(response, status=status_code)


class StoresView(generics.ListCreateAPIView):
    serializer_class = StoresSerializer
    JWTAuthentication = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsMerchant)
    # _logger.info(logger_name + ":-" + " Someone is trying to access Store page")
    _logger.info(event='Stores View !', into='Store View page')

    def get_queryset(self):
        # _logger.info(logger_name + ":-" + self.request.user.username + " " + "is trying to access Store page")
        _logger.info(event='Stores View !', user=self.request.user.username, role=return_role(self.request.user),
                     message='is trying to access Store page')
        profile = Profile.objects.get(user=self.request.user)
        stores = Stores.objects.filter(merchant=profile)
        if stores:
            # _logger.info(logger_name + ":-" + self.request.user.username + " " + "has accessed stores")
            _logger.info(event='Stores View !', user=self.request.user.username, role=return_role(self.request.user),
                         message='has accessed stores')
        else:
            # _logger.info(logger_name + ":-" + self.request.user.username + " " + "was not able to access stores")
            _logger.warning(event='Stores View !', user=self.request.user.username, role=return_role(self.request.user),
                            message='was not able to access stores')
        return stores

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(merchant=profile)
        # _logger.info(logger_name + ":-" + self.request.user.username + " " + "created a new store")
        _logger.info(event='Stores View !', user=self.request.user.username, role=return_role(self.request.user),
                     message='created a new store')


class ItemsView(generics.ListCreateAPIView):
    # _logger.info(logger_name + ":-" + " Someone is trying to access Items page")
    _logger.info(event='Items View !', message='Someone is trying to access Items page')
    serializer_class = ItemSerializers
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsMerchant)

    # queryset = Items.objects.all()

    def get_queryset(self):
        # _logger.info(logger_name + ":-" + self.request.user.username + " " + "is trying to access Items page")
        _logger.info(event='Items View !', user=self.request.user.username, role=return_role(self.request.user),
                     message='is trying to access Items page')
        profile = Profile.objects.get(user=self.request.user)
        items = Items.objects.filter(stores__merchant=profile)
        if items:
            # _logger.info(logger_name + ":-" + self.request.user.username + " " + "has accessed items")
            _logger.info(event='Items View !', user=self.request.user.username, role=return_role(self.request.user),
                         message='has accessed items')
        else:
            # _logger.info(logger_name + ":-" + self.request.user.username + " " + "was not able to access items")
            _logger.warning(event='Items View !', user=self.request.user.username, role=return_role(self.request.user),
                            message='was not able to access items')
        return items

    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user)
    #     serializer.save(stores__merchant=profile)


class PlaceOrderView(generics.ListCreateAPIView):
    # _logger.info(logger_name + ":-" + "Someone is trying to access Place Order Page")
    _logger.info(event='Place Order !', message='Someone is trying to access Place Order Page')
    serializer_class = OrderSerializer
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def get_queryset(self):
        orders = Orders.objects.filter(user=self.request.user)
        if orders:
            # _logger.info(logger_name + ":-" + self.request.user.username + " " + "has accessed their placed orders")
            _logger.info(event='Place Order !', user=self.request.user.username, role=return_role(self.request.user),
                         message='has accessed their placed orders')
        else:
            # _logger.info(
            #     logger_name + ":-" + self.request.user.username + " " + "was not able to access their placed orders")
            _logger.warning(event='Place Order !', user=self.request.user.username, role=return_role(self.request.user),
                            message='was not able to access their placed orders')
        return orders

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # import ipdb; ipdb.set_trace()
        pk = self.request.user.pk
        create_an_order.delay(pk, serializer.data)
        # _logger.info(logger_name + ":-" + self.request.user.username + " " + "created a new order - Celery task")
        _logger.info(event='Place Order !', user=self.request.user.username, role=return_role(self.request.user),
                     message='created a new order - Celery task')


class SeeOrderView(generics.ListAPIView):
    # _logger.info(logger_name + ":-" + "Someone is trying to access See Order Page")
    _logger.info(event='Place Order !', message='Someone is trying to access See Order Page')
    serializer_class = OrderSerializer
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsMerchant)

    # def get_queryset(self):
    #     orders = Orders.objects.filter(user=self.request.user)
    #     return orders
    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        orders = Orders.objects.filter(merchant=profile)
        if orders:
            # _logger.info(logger_name + ":-" + self.request.user.username + " " + "has accessed their store's orders")
            _logger.info(event='Place Order !', user=self.request.user.username, role=return_role(self.request.user),
                         message="has accessed their store's orders")
        else:
            _logger.info(logger_name + ":-" + self.request.user.username + " " + "was not able to access their store's "
                                                                                 "orders")
            _logger.warning(event='Place Order !', user=self.request.user.username, role=return_role(self.request.user),
                            message="was not able to access their store's orders")
        return orders


class UserListView(generics.ListCreateAPIView):
    # _logger.info(logger_name + ":-" + "Someone is trying to access See Order Page")
    _logger.info(event='View Users !', message='Someone is trying to access the Users Page')
    serializer_class = UserViewSerializers
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        current_profile_role = return_role(user)
        if current_profile_role == "Merchant":
            people = User.objects.filter(profile__role=2)
            _logger.info(event='View Users !', user=self.request.user.username, role=return_role(self.request.user),
                         message=" accessed the Customers List")
        elif current_profile_role == 'Customer':
            people = User.objects.filter(profile__role=1)
            _logger.info(event='View Users !', user=self.request.user.username, role=return_role(self.request.user),
                         message="accessed the Merchants List")
        else:
            people = User.objects.filter(profile__role=1)
            _logger.error(event='View Users !', user=self.request.user.username, role=return_role(self.request.user),
                          message="accessed the Merchants List but not in the normal method")
        return people
