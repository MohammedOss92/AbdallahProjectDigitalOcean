from django.db import models

# Create your models here.
class Nokat(models.Model):
    NokatTypes = models.CharField(max_length=100, null=True)
    new_nokat = models.CharField(max_length=2,default=1)
    NokatName = models.CharField(max_length=1000, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    new_msgs_text = models.CharField(max_length=2, null=True, default=1)
    created_at_new_msgs_text = models.DateField(null=True)
    updated_at_new_msgs_text = models.DateField(null=True)
    my_time_auto = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.NokatTypes