from FatmugApp.Models import PurchaseOrder, Vendors
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, ExpressionWrapper, fields, F
from ..Serializers import PurchaseOrderSerializer, PurchaseOrderInputSerializer
from django.db import transaction
from datetime import datetime, timedelta
from Utils import (
    on_time_delivery_rate,
    fulfillment_rate,
    avg_quality_rate,
    avg_response_time,
)
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import (
    permission_classes,
    api_view,
    authentication_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_orders(request):
    purchase_orders = PurchaseOrder.objects.all()
    purchase_orders_serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response(status=status.HTTP_200_OK, data=purchase_orders_serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order(request, po_id):
    try:
        purchase_orders = PurchaseOrder.objects.get(id=int(po_id))
        if purchase_orders:
            purchase_orders_serializer = PurchaseOrderSerializer(purchase_orders)
            return Response(
                status=status.HTTP_200_OK, data=purchase_orders_serializer.data
            )
    except PurchaseOrder.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"message": "Purchase Order doesn't exists."},
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_purchase_order(request):
    with transaction.atomic():
        po_seriaizer = PurchaseOrderInputSerializer(data=request.data)
        if po_seriaizer.is_valid():
            po_seriaizer.save()
            vendor_id = po_seriaizer.validated_data.get("vendor_id", None)
            po_status = po_seriaizer.validated_data.get("status", None)
            quality_rating = po_seriaizer.validated_data.get("quality_rating", None)
            acknowledgment_date = po_seriaizer.validated_data.get(
                "acknowledgment_date", None
            )

            if po_status and str(po_status).lower() == "completed":
                success = on_time_delivery_rate(vendor_id=vendor_id)
                if success.get("success") is False:
                    raise serializers.ValidationError({"error":success.get("message")})

            if quality_rating is not None and str(po_status).lower() == "completed":
                success = avg_quality_rate(vendor_id=vendor_id)
                if success.get("success") is False:
                    raise serializers.ValidationError({"error":success.get("message")})

            if po_status and vendor_id:
                success = fulfillment_rate(vendor_id=vendor_id)
                if success.get("success") is False:
                    raise serializers.ValidationError({"error":success.get("message")})

            if acknowledgment_date:
                success = avg_response_time(vendor_id)
                if success.get("success") is False:
                    raise serializers.ValidationError({"error":success.get("message")})

            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Purchase Order created successfully."},
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=po_seriaizer.errors
            )


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_purchase_order(request, po_id):
    try:
        with transaction.atomic():
            po_instance = PurchaseOrder.objects.get(id=int(po_id))
            po_seriaizer = PurchaseOrderInputSerializer(
                instance=po_instance, data=request.data
            )
            if po_seriaizer.is_valid():
                vendor_id = po_seriaizer.validated_data.get(
                    "vendor_id", po_instance.vendor_id
                )
                po_seriaizer.update(po_instance, po_seriaizer.validated_data)
                po_status = po_seriaizer.validated_data.get(
                    "status", po_instance.status
                )
                quality_rating = po_seriaizer.validated_data.get(
                    "quality_rating", po_instance.quality_rating
                )
                acknowledgment_date = po_seriaizer.validated_data.get(
                    "acknowledgment_date", po_instance.acknowledgment_date
                )

                if po_status and str(po_status).lower() == "completed":
                    success = on_time_delivery_rate(
                        vendor_id=vendor_id
                    )
                    if success.get("success") is False:
                        raise serializers.ValidationError({"error":success.get("message")})

                if quality_rating and str(po_instance.status).lower() == "completed":
                    success = avg_quality_rate(vendor_id=vendor_id)
                    if success.get("success") is False:
                        raise serializers.ValidationError({"error":success.get("message")})

                if po_status and vendor_id:
                    success = fulfillment_rate(vendor_id)
                    if success.get("success") is False:
                        raise serializers.ValidationError({"error":success.get("message")})

                if acknowledgment_date:
                    success = avg_response_time(vendor_id=vendor_id)
                    if success.get("success") is False:
                        raise serializers.ValidationError({"error":success.get("message")})

                return Response(
                    status=status.HTTP_200_OK,
                    data={"message": "Purchase Order updated successfully."},
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data=po_seriaizer.errors
                )
    except PurchaseOrder.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"message": "PO doesn't exists."},
        )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_purchase_order(request, po_id):
    try:
        with transaction.atomic():
            po_instance = PurchaseOrder.objects.get(id=int(po_id))
            if po_instance:
                po_instance.delete()
                return Response(
                    status=status.HTTP_200_OK,
                    data={"message": "Purchase Order deleted successfully."},
                )
            else:
                return Response(
                    status=status.HTTP_200_OK,
                    data={"message": "Purchase Order doesn't exists."},
                )
    except PurchaseOrder.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"message": "PO doesn't exists."},
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_acknowledge(request, po_id):
    try:
        po_instance = PurchaseOrder.objects.get(id=int(po_id))
        po_seriaizer = PurchaseOrderInputSerializer(
            instance=po_instance, data=request.data
        )
        with transaction.atomic():
            if po_seriaizer.is_valid():
                po_seriaizer.update(po_instance, po_seriaizer.validated_data)
                acknowledgment_date = po_seriaizer.validated_data.get(
                    "acknowledgment_date", po_instance.acknowledgment_date
                )
                vendor_id = po_seriaizer.validated_data.get(
                    "vendor_id", po_instance.vendor.id
                )
                if acknowledgment_date:
                    success = avg_response_time(vendor_id=vendor_id)
                    if success.get("success") is False:
                        raise ValidationError(success.get("message"))
                return Response(
                    status=status.HTTP_200_OK,
                    data={"message": "Purchase Order updated successfully."},
                )
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=po_seriaizer.errors
            )
    except PurchaseOrder.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"message": "PO doesn't exists."},
        )
