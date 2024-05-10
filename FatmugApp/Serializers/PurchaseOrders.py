from rest_framework import serializers
from ..Models import PurchaseOrder
from ..Serializers.Vendors import VendorSerializer 
from ..Models import Vendors
from datetime import datetime

class PurchaseOrderInputSerializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(required=False,write_only=True)
    class Meta:
        model = PurchaseOrder
        fields= ('id','po_number','vendor_id','delivery_date','items','quantity','status','quality_rating','issue_date','acknowledgment_date')

    def validate(self, data):
        vendor_id = data.get('vendor_id', None)
        if vendor_id is not None:
            try :
                Vendors.objects.get(id=int(vendor_id))
            except Vendors.DoesNotExist:
                raise serializers.ValidationError({"vendor_id":"Vendor Doesn't exists."})
        return data
    
    def create(self, validated_data):
        create_po = PurchaseOrder(**validated_data)
        vendor_id = validated_data.pop('vendor_id', None)
        issue_date = validated_data.get('issue_date', None)
        acknowledgment_date = validated_data.get('acknowledgment_date', None)
        status = validated_data.get('status', None)
        quality_rating = validated_data.get('quality_rating', None)
        delivery_date = validated_data.get('delivery_date', None)

        if status and str(status).lower() == "completed":
            if vendor_id is None:
                raise serializers.ValidationError({"vendor_id":"Vendor deatils didn't provided.But making Purchase Order complete"})
            # if acknowledgment_date is None:
            #     raise serializers.ValidationError({"acknowledgment_date":"Acknowledgment Date deatils didn't provided.But making Purchase Order complete"})
            # if issue_date is None:
            #     raise serializers.ValidationError({"issue_date":"Issue Date deatils didn't provided.But making Purchase Order complete"})

        if quality_rating:
            if status and str(status).lower() != "completed":
                raise serializers.ValidationError({"quality_rating":"Quality Rating Provided with Purchase Order Complete."})

        if vendor_id is not None:
            vendor = Vendors.objects.get(id=vendor_id)
            create_po.vendor = vendor

        if acknowledgment_date and not issue_date :
                raise serializers.ValidationError({"issue_date":"Acknowledgment Date is provided but not issue Date."})
        
        if acknowledgment_date and issue_date:
            if acknowledgment_date < issue_date:
                    raise serializers.ValidationError({"issue_date":"issue Date should not greater then Acknowledgment Date."})
        
        if issue_date and delivery_date:
            if delivery_date < issue_date:
                raise serializers.ValidationError({"issue_date":"Please provide issue Date correctly."})
            
        if issue_date:
            if vendor_id is None:
                raise serializers.ValidationError({"vendor_id":"Vendor deatils didn't provided."})

        if status and str(status).lower() == "completed" and vendor_id is None:
            raise serializers.ValidationError({"vendor_id":"Vendor deatils didn't provided.But making Purchase Order complete"})
        
        if quality_rating and str(status).lower() != "completed":
            raise serializers.ValidationError({"error":"Quality Rate provided but Purchase Order is Incomplete."})
        
        # create_po.save()
        return  create_po

    def update(self, instance, validated_data):
        vendor_id = validated_data.get('vendor_id',None)
        if vendor_id:
            vendor = Vendors.objects.get(id=vendor_id)
            instance.vendor = vendor
        else:
            instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.po_number = validated_data.get('po_number', instance.po_number)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.items = validated_data.get('items', instance.items)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        instance.issue_date = validated_data.get('issue_date', instance.issue_date)
        instance.acknowledgment_date = validated_data.get('acknowledgment_date', instance.acknowledgment_date)
        


        if instance.status and str(instance.status).lower() == "completed":
            if not instance.vendor:
                raise serializers.ValidationError({"vendor_id":"Vendor deatils didn't provided.But making Purchase Order complete"})
            # if not instance.acknowledgment_date:
            #     raise serializers.ValidationError({"acknowledgment_date":"Acknowledgment Date deatils didn't provided.But making Purchase Order complete"})
            # if not instance.issue_date:
            #     raise serializers.ValidationError({"issue_date":"Issue Date deatils didn't provided.But making Purchase Order complete"})

        if instance.acknowledgment_date and not instance.issue_date :
                raise serializers.ValidationError({"issue_date":"Acknowledgment Date is provided but not issue Date."})
        
        if instance.issue_date and instance.delivery_date:
            if instance.delivery_date < instance.issue_date :
                raise serializers.ValidationError({"issue_date":"Please provide issue Date correctly."})

        if instance.acknowledgment_date and instance.issue_date:
            if instance.acknowledgment_date < instance.issue_date:
                    raise serializers.ValidationError({"issue_date":"issue Date should not greater then Acknowledgment Date."})

        if instance.issue_date and not instance.vendor:
            raise serializers.ValidationError({"vendor_id":"Vendor deatils didn't provided."})
            
        # instance.save()  
        return instance
    
class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    class Meta:
        model = PurchaseOrder
        fields= "__all__"
