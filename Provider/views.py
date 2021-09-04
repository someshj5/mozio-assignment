from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from Provider.models import User
from django.contrib.auth import login, logout, authenticate
import jwt
# Create your views here.


def get_custom_response(success=False, message='something went wrong', data=None, status=400):

    response = {
        'success': success,
        'message': message,
        'data': data
    }
    return Response(response, status=status)


def timestamp():
    return int(datetime.timestamp(datetime.now()))


class ProviderView(APIView):
    @permission_classes((permissions.AllowAny,))
    def get(self, request):
        """ This is the method for fetching all Providers
        Returns:
            json: returns all the Providers
        """
        try:
            users = User.objects.all()
            # print(users)
            
            if users:
                serializer = UserSerializer(users,many=True)
                custom_response = get_custom_response(
                    success=True, message="Sucessful", data=serializer.data, status=200)
                return custom_response
            else:
                error = get_custom_response()
                return error
        except Exception as e:
            print(e)
            error = get_custom_response()
            return error
            
    @permission_classes((permissions.AllowAny,))
    def post(self,request):
        try:
            payload = {
                "email": request.data.get('email'),
                "username": request.data.get('username'),
                "first_name": request.data.get('first_name'),
                "last_name": request.data.get('last_name'),
                "phone_number": request.data.get('phone_number'),
                "currency": request.data.get('currency'),
                "password":request.data.get('password'),
                "language": request.data.get('language')
            }
            print(payload)
            serializer = UserSerializer(data=payload)
            # print(serializer, 'serializers')
            if serializer.is_valid():
                user = serializer.save()
                print(user.password)
                user.set_password(request.data.get('password'))
                user.save()
                custom_response = get_custom_response(
                    success=True, message="Sucessful", data=serializer.data, status=200)
                return custom_response
            else:
                error = get_custom_response(data=serializer.errors)
                return error
           
        except Exception as e:
            print(e, '-------')
            error = get_custom_response()
            return error


class EditProvider(APIView):

    def get(self, request, pk):
        """
        :param pk: the primary key of Provider
        :param request: request for data
        :return: returns the response
        """
        try:
            user = User.objects.get(pk=pk)
            if user:
                serializer = UserSerializer(user)
                custom_response = get_custom_response(
                    success=True, message="Sucessful", data=serializer.data, status=200)
                return custom_response
            else:
                raise ValueError
        except ValueError:
            error = get_custom_response()
            return error

    def put(self,request,pk):
        """
        :param pk: the primary key of Provider
        :param request: request for data
        :return: returns the edited response
        """
        try:
            user = User.objects.get(pk=pk)
            if not user:
                error = get_custom_response(data="No such Provider")
                return error

            else:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    provider_ser = serializer.update(instance=user, validated_data=request.data)
                    custom_response = get_custom_response(
                    success=True, message="Sucessful", data=serializer.data, status=200)
                    return custom_response

        except Exception as e:
            print(e, '-------')
            error = get_custom_response()
            return error

    def delete(self, request, pk):
        """
        :param pk: the primary key of Provider
        :param request: request for data
        :return: returns the response
        """
        try:
            provider = User.objects.get(pk=pk)
            if provider:
                # print(provider)
                provider.delete()
                custom_response = get_custom_response(
                    success=True, message="Provider deletion Sucessful", status=200)
                return custom_response
            else:
                error = get_custom_response(data="No such Provider")
                return error
        except Exception as e:
            print(e, '-------')
            error = get_custom_response()
            return error

@api_view(['POST'])
def loginView(request):
    try:
        username=request.data.get('username')
        user1 = User.objects.get(username=username)
        password=request.data.get('password')
        user = authenticate(username=username, password=password)
        print('160',user)
        if user:
            payload = {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
            jwt_token = jwt.encode(
                payload, "SECRET_KEY",
                algorithm="HS256")
            login(request, user)
            custom_response = get_custom_response(success=True,data=jwt_token,message="Authentication Sucessful",status=200)
            return custom_response
        else:
            error = get_custom_response(message='User not authentcated')
            return error
    except Exception as e:
        print(e)
        error = get_custom_response()
        return error
