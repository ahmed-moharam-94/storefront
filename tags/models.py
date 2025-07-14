from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    label = models.CharField(max_length=255)


# to be able to use this model as a generic model in any app 
# we should not make the model depends on a specific model 
# so we will use Content_type that is defined in settings
class TaggedItem(models.Model): # Tag  <------- TaggedItem ---------> Content_Type 
    # define what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # 1) define content type to find which table you will deal with
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 2) define which record using id
    object_id = models.PositiveIntegerField()
    # 3) get the received object
    content_object = GenericForeignKey()



