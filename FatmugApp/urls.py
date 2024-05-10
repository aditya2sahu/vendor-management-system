from django.contrib import admin
from django.urls import path,include
from .Views import vendors,get_vendor,update_vendor,add_vendor,delete_vendor,add_purchase_order,purchase_orders,purchase_order,update_purchase_order,delete_purchase_order,vendor_acknowledge

urlpatterns = [
    # vendor CRUD Oerations
    path('vendors',add_vendor,name="add_vendor"),
    path('vendors/',vendors,name="vendors"),
    path('vendor/<int:vendor_id>',get_vendor,name="vendor_by_id"),
    path('vendor/update/<int:vendor_id>',update_vendor,name="update_vendor"),
    path('vendor/delete/<int:vendor_id>',delete_vendor,name="delete_vendor"),

    # Purchase Order CRUD Operation
    path('purchase_orders/',purchase_orders,name="purchase_orders"),
    path('purchase_orders',add_purchase_order,name="add_purchase_order"),
    path('purchase_order/<int:po_id>',purchase_order,name="purchase_order_by_id"),
    path('purchase_order/update/<int:po_id>',update_purchase_order,name="update_purchase_order"),
    path('purchase_order/delete/<int:po_id>',delete_purchase_order,name="delete_purchase_orders"),
    path("purchase_order/<int:po_id>/acknowledge",vendor_acknowledge
         ,name="vendor_acknowledgement")
]
