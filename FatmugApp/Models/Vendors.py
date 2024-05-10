
from django.db import models

class Vendors(models.Model):
    name = models.CharField(max_length=200,blank=True)
    contact_details = models.TextField(blank=True)
    address = models.TextField(blank=True)
    vendor_code =  models.CharField(blank=True,max_length=10)
    on_time_delivery_rate = models.FloatField(null=True,blank=True)
    quality_rating_avg = models.FloatField(null=True,blank=True)
    average_response_time = models.FloatField(null=True,blank=True)
    fulfillment_rate = models.FloatField(null=True,blank=True)
    def __str__(self):
        return self.name + str(self.id)
