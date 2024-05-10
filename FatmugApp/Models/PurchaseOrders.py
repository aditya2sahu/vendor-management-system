from django.db import models
from .Vendors import Vendors

class PurchaseOrder(models.Model):
    po_number = models.CharField(unique=True,max_length=100,blank=True)
    vendor= models.ForeignKey(Vendors,on_delete=models.DO_NOTHING,null=True,blank=True)
    delivery_date = models.DateTimeField(blank=True)
    items = models.JSONField(blank=True)
    quantity = models.IntegerField(blank=True)
    status_choices = [
        ('Pending', 'Pending - Waiting for action'),
        ('In Progress', 'In Progress - Currently being worked on'),
        ('Completed', 'Completed - Finished successfully'),
    ]
    status = models.CharField(max_length=20, choices=status_choices,blank=True)
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date = models.DateTimeField(null=True,blank=True)
    acknowledgment_date = models.DateTimeField(null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.po_number