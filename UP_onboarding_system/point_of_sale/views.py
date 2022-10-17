from rest_framework.decorators import api_view, permission_classes

from .permissions import IsMerchant, IsConsumer
from .serializers import *
import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.reverse import reverse_lazy


@api_view(['GET'])
def ApiHomepage(request, format=None):
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
    return Response(status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

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
            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

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
            return Response(response, status=status_code)


class StoresView(generics.ListCreateAPIView):
    serializer_class = StoresSerializer
    JWTAuthentication = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsMerchant)

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        stores = Stores.objects.filter(merchant=profile)
        return stores

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(merchant=profile)


class ItemsView(generics.ListCreateAPIView):
    serializer_class = ItemSerializers
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsMerchant)
    #queryset = Items.objects.all()

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        items = Items.objects.filter(stores__merchant=profile)
        return items

    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user)
    #     serializer.save(stores__merchant=profile)


class PlaceOrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def get_queryset(self):
        orders = Orders.objects.filter(user=self.request.user)
        return orders

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SeeOrderView(generics.ListAPIView):
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
        return orders


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserViewSerializers
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsMerchant)
    queryset = User.objects.filter(profile__role=2)
