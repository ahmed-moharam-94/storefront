from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=obj_id
            )


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label


# to define a generic relationship you have to define 3 required fields
# 1) content_type: ForeignKey(ContentType)
# 2) object_id: PositiveIntegerField()
# 3) content_object: GenericForeignKey()
class TaggedItem(models.Model):
    # 3 required fields to define a generic relationship
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # override objects to use TaggedItemManager()
    objects = TaggedItemManager()
