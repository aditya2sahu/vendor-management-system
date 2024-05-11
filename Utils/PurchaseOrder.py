from FatmugApp.Models import Vendors, PurchaseOrder
from django.db.models import F, fields, ExpressionWrapper, aggregates, Sum
from datetime import datetime, timedelta,timezone
from django.db import transaction
from django.db.models.functions import Extract


def on_time_delivery_rate(vendor_id):
    try:
        with transaction.atomic():
            completed_po_vendor = PurchaseOrder.objects.filter(
                vendor__id=vendor_id, status="Completed"
            ).count()
            po_before_date = PurchaseOrder.objects.filter(
                vendor__id=vendor_id, delivery_date__lte=datetime.today().date()
            ).count()
            if completed_po_vendor != 0:
                on_time_delivery_rate = po_before_date / completed_po_vendor
                Vendors.objects.update(on_time_delivery_rate=on_time_delivery_rate)
            else:
                Vendors.objects.update(on_time_delivery_rate=0.0)
            context = {"message": "Successfully commit", "success": True}

            return context

    except Exception as e:
        print("on_time_delivery_rate",e)
        context = {"message": str(e), "success": False}
        return context


def avg_quality_rate(vendor_id):
    try:
        with transaction.atomic():
            completed_po_vendor = PurchaseOrder.objects.filter(
                vendor__id=vendor_id, status="Completed"
            ).count()
            total_quality_rating = PurchaseOrder.objects.filter(
                vendor__id=vendor_id, status="Completed"
            ).aggregate(quality_rating=Sum("quality_rating"))

            if completed_po_vendor == 0:
                Vendors.objects.update(quality_rating_avg=0.0)
            else:
                quality_rating_avg = (
                    total_quality_rating.get("quality_rating", 0) / completed_po_vendor
                )
                Vendors.objects.update(quality_rating_avg=quality_rating_avg)
            context = {"message": "Successfully commit", "success": True}
            return context
    except Exception as e:
        print("avg_quality_rate",e)
        context = {"message": str(e), "success": False}
        return context


def avg_response_time(vendor_id):
    try:
        purchase_orders = (
            PurchaseOrder.objects.filter(
                vendor__id=int(vendor_id),
                acknowledgment_date__isnull=False,
            )
            .annotate(
                difference=ExpressionWrapper(
                    F("acknowledgment_date") - F("issue_date"),
                    output_field=fields.DurationField(),
                )
            )
            .aggregate(
                total_difference_in_days=Sum('difference')
            )
        )
        with transaction.atomic():
            total_difference_in_days = purchase_orders.get('total_difference_in_days',None)
            issued_date_to_vendor = PurchaseOrder.objects.filter(vendor__id=vendor_id,issue_date__isnull=False).count()
            if issued_date_to_vendor == 0:
                Vendors.objects.update(average_response_time=0.0)
            else:
                avg_response_time = total_difference_in_days.days / issued_date_to_vendor
                Vendors.objects.update(average_response_time=avg_response_time)
            context = {"message": "Successfully commit", "success": True}
            return context
    except Exception as e:
        print("avg_response_time",e)
        context = {"message": str(e), "success": False}
        return context


def fulfillment_rate(vendor_id):
    try:
        with transaction.atomic():
            po_without_issue = PurchaseOrder.objects.filter(
                issue_date__isnull=True, vendor__id=int(vendor_id), status="Completed"
            ).count()
            po_with_issue = PurchaseOrder.objects.filter(
                vendor__id=vendor_id, issue_date__isnull=False
            ).count()
            if po_with_issue == 0:
                vendor = Vendors.objects.update(fulfillment_rate=0.0)
            else:
                fulfillment_rate = po_without_issue / po_with_issue
                vendor = Vendors.objects.get(id=vendor_id)
                vendor.fulfillment_rate = fulfillment_rate
                vendor.save()
            context = {"message": "Successfully commit", "success": True}
            return context
    except Exception as e:
        print("fulfillment_rate",e)
        context = {"message": str(e), "success": False}
        return context
