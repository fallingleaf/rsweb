from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from serializers import UserSerializer, SignUpSerializer, TokenSerializer, ContactSerializer
from jupiter.models import AuthUser


# Create your views here.
# class based view
class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def signup(request, format=None):
    serializer = SignUpSerializer(data=request.data)
    response_serializer = UserSerializer
    if serializer.is_valid():
        serializer.save()
        return Response(response_serializer(serializer.data).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def contact(request, format=None):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(dict(message="Thank you for contacting me!"), status=status.HTTP_200_OK)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    """
    Check django credentials and return token 
    if credentials is valid and authenticated
    Call login api to register user
    Accept: username and password
    Return: token's object key
    """
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer
    token_model = Token
    response_serializer = TokenSerializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        return Response(
            self.response_serializer(self.token).data, status=status.HTTP_200_OK
        )

    def get_error_response(self):
        return Response(
            self.serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.DATA)
        if not self.serializer.is_valid():
            return self.get_error_response()
        self.login()
        return self.get_response()


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)

# class FacebookLogin(SocialLogin):
#     adapter_class = FacebookOAuth2Adapter

# class UserList(APIView):
#     """
#     List all users or create new one
#     """
#     def get(self, request, format=None):
#         users = AuthUser.objects.all()
#         serializers = UserSerializer(users, many=True)
#         return Response(serializers.data)

#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserDetail(APIView):
#     """
#         Retrieve, update or delete user
#     """
#     def get_object(self, pk):
#         try:
#             user = AuthUser.objects.get(pk=pk)
#             return user
#         except AuthUser.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         serializer = UserSerializer(self.get_object(pk))
#         return Response(serializer.data)

#     def post(self, request, pk, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk, format=None):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# use function views
# @api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, IsAdminUser,))
# def user_list(request, format=None):
#     """
#     List all users, or create new one
#     """
#     if request.method == "GET":
#         users = AuthUser.objects.all()
#         serializers = UserSerializer(users, many=True)
#         return Response(serializers.data)

#     elif request.method == "POST":
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete user
#     """
#     try:
#         user = AuthUser.objects.get(pk=pk)
#     except AuthUser.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
