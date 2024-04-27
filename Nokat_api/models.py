from django.db import models
from django.conf import settings
from django.db.models.signals import post_init

from django.dispatch import receiver
import os


# Create your models here.
class Nokat(models.Model):
    NokatTypes = models.CharField(max_length=1000, null=True)
    new_nokat = models.CharField(max_length=2,default=1)
    NokatName = models.CharField(max_length=1000, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    new_msgs_text = models.CharField(max_length=2, null=True, default=1)
    created_at_new_msgs_text = models.DateField(null=True)
    updated_at_new_msgs_text = models.DateField(null=True)
    my_time_auto = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.NokatName




class ImagesNokat(models.Model):
    #new_nokat = models.CharField(max_length=2, null=True, choices=(('0', '0'), ('1', '1')))
    #new_img = models.BooleanField(default=True)
    new_img = models.IntegerField(default=1, choices=[(0, '0'), (1, '1')])
    pic = models.ImageField(upload_to='nokat/')
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    #new_msgs_text = models.CharField(max_length=1, null=True, choices=(('0', '0'), ('1', '1')))
    img_show= models.IntegerField(default=1, choices=[(0, '0'), (1, '1')])
    created_at_new_msgs_text = models.DateField(null=True)
    updated_at_new_msgs_text = models.DateField(null=True)
    my_time_auto = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.image_url

@receiver(post_init, sender=ImagesNokat)
def create_nokat_folder(sender, instance, **kwargs):
    # «· √ﬂœ „‰ √‰ «·„Ã·œ €Ì— „ÊÃÊœ »«·›⁄·
    if not os.path.exists('media/nokat'):
        # ≈‰‘«¡ «·„Ã·œ ≈–« ·„ Ìﬂ‰ „ÊÃÊœ«
        os.makedirs('media/nokat')    