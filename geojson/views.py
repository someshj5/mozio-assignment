from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from geojson.serializers import RegionSerializer,PolygonCoordinatesSerializer
from geojson.models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
# Create your views here.
import jwt
from django.views.decorators.csrf import csrf_exempt

def get_custom_response(success=False, message='something went wrong', data=None, status=400):

    response = {
        'success': success,
        'message': message,
        'data': data
    }
    return Response(response, status=status)

class PolygonView(APIView):
    @permission_classes((permissions.AllowAny,))
    def get(self,request):
        """ This is the method for fetching all Polygon based on Latitude Longitude
        Returns:
            json: returns all the Regions
        """
        try:
            token = request.headers.get('Authorization')
            if token:
                key = 'SECRET_KEY'
                decoded = jwt.decode(token, key, algorithms=['HS256'])
                lat = request.GET.get('latitude')
                lng = request.GET.get('longitude')
                polygon = PolygonCoordinates.objects.filter(latitude=lat,longitude=lng)
                if bool(polygon):
                    polygonslist=[]
                    for i in polygon:
                        serializer = PolygonCoordinatesSerializer(i)
                        polygonslist.append(serializer.data)

                    data = get_custom_response(success=True,message="Successfull",data=polygonslist)
                    return data
                else:
                    error = get_custom_response(message='Not found')
                    return error
            else:
                error = get_custom_response(message='token is needed to proceed! Not Authenticated')
                return error
        except Exception as e:
            error = get_custom_response()
            return error

    @csrf_exempt
    def post(self,request):
        try:
            token = request.headers.get('Authorization')
            coordinates = request.data['coordinates']
            if token:
                key = 'SECRET_KEY'
                decoded = jwt.decode(token, key, algorithms=['HS256'])
                payload = {
                    "email": request.data['email'],
                    "price": request.data['price'],
                    "provider": decoded["id"]
                }
                serializer = RegionSerializer(data=payload)
                if serializer.is_valid():
                    polygon=serializer.save()
                    # polygon_id = serializer.data["id"]
                    for co_ordinate in coordinates:
                        [latitude,longitude]=co_ordinate
                        poly_coordinates = PolygonCoordinates.objects.create(latitude=latitude,longitude=longitude,Polygon=polygon)
                    custom_response = get_custom_response(
                        success=True, message="Sucessful", data=serializer.data, status=200)
                    return custom_response
            else:
                custom_response = get_custom_response(data=serializer.errors)
                return custom_response

        except Exception as e:
            error = get_custom_response()
            return error

class PolygonApi(APIView):
    def get(self,request,pk):
        """

        Args:
            request(get): [description]
            pk ([type]): [description]
        """
        try:
            polygon = Polygon.objects.get(id=pk)
            if polygon:
                serializer = RegionSerializer(data=polygon.__dict__)
                if serializer.is_valid():
                    custom_response = get_custom_response(
                            success=True, message="Sucessful", data=serializer.data, status=200)
                    return custom_response
                else:
                    error = get_custom_response(data=serializer.errors)
                    return error
            else:
                error = get_custom_response()
                return error
        except Exception as e:
            error = get_custom_response()
            return error

    def delete(self,request,pk):
        try:
            polygon = Polygon.objects.get(pk)
            if polygon:
                polygon.delete()
                custom_response = get_custom_response(success=True, message="Sucessful", status=200)
                return custom_response
        except Exception as e:
            error = get_custom_response()
            return error

    def put(self,request,pk):
        try:
            polygon = Polygon.objects.get(pk)
            if polygon:
                serializer = RegionSerializer(data=request.data)
                if serializer.is_valid():
                    PolygonSer = RegionSerializer.update(instance=polygon,validated_data=request.data)
                    custom_response = get_custom_response(
                    success=True, message="Sucessful", data=serializer.data, status=200)
                    return custom_response

        except Exception as e:
            error = get_custom_response()
            return error

