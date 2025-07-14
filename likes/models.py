from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey




class LikedItem(models.Model): # User <----------- LikedItem -------------> Content Type
    # define what user likes what object
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # define which table
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # define the which id
    object_id = models.PositiveIntegerField()
    # received object
    content_object = GenericForeignKey()
