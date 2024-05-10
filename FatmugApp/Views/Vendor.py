from django.shortcuts import  render
from rest_framework.response import Response
from rest_framework import status
from ..Models import Vendors
from ..Serializers import VendorSerializer,VendorInputSerializer
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendors(request):
    try:
        vendors = Vendors.objects.all()
        serializer = VendorSerializer(vendors,many=True)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={"error":str(e)})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_vendor(request,vendor_id):
    vendors = Vendors.objects.get(id=int(vendor_id))
    if vendors:
        serializer = VendorSerializer(vendors)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"Vendor doesn't exists."})

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_vendor(request):
    with transaction.atomic():
        vendor_serializer = VendorInputSerializer(data=request.data)
        if vendor_serializer.is_valid():
            vendor_serializer.save()
            return Response(status=status.HTTP_201_CREATED,data={"message":"Vendor created successfully"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=vendor_serializer.errors)
        
@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_vendor(request,vendor_id):
    with transaction.atomic():
        vendor_instance = Vendors.objects.get(id=int(vendor_id))
        vendor_serializer = VendorInputSerializer(vendor_instance,data=request.data)
        if vendor_serializer.is_valid():
            vendor_serializer.update(vendor_instance,validated_data=request.data)
            return Response(status=status.HTTP_200_OK,data={"message":"Vendor updated successfully."})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=vendor_serializer.errors)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_vendor(request,vendor_id):
    with transaction.atomic():
        vendor_instance = Vendors.objects.get(id=int(vendor_id))
        if vendor_instance:
            vendor_instance.delete()
            return Response(status=status.HTTP_200_OK,data={"message":"Vendor deleted successfully."})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"Vendor doesn't exists."})