from rest_framework import serializers
from ..Models import Vendors

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields= '__all__'

class VendorInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields= ("name","contact_details","address","vendor_code")
    
    def create(self, data):
        vendor = Vendors.objects.create(
            name=data.get("name"),
            contact_details=data.get("contact_details"),
            vendor_code=data.get("vendor_code"),
            address=data.get("address"),
        )
        return vendor

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.contact_details = validated_data.get("contact_details",instance.contact_details)
        instance.address = validated_data.get("address",instance.address)
        instance.vendor_code = validated_data.get("vendor_code",instance.vendor_code)
        instance.save()
        return instance