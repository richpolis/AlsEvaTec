import re
import datetime
from unidecode import unidecode
from django.utils import timezone

from alsevatec.settings import TIME_ZONE

def slug_generator(text, model, *args, **kwargs):
    """
    Function used to generate a slug based on text passed and checking if slug generated is not stored in bd to the model
    """
    slug = re.sub("\W+", "-", text)
    if slug.startswith("_") or slug.startswith("-"):
        slug = slug[1:]

    if slug.endswith("_") or slug.endswith("-"):
        slug = slug[:-1]

    slug = unidecode(slug)
    slug = slug.lower()
    tmp_slug = slug
    i = 1
    if hasattr(model, 'slug'):
        while model.objects.filter(slug=tmp_slug).exists():
            tmp_slug = slug + "-" + str(i)
            i += 1
    elif hasattr(model, 'username'):
        while model.objects.filter(username=tmp_slug).exists():
            tmp_slug = slug + "-" + str(i)
            i += 1
    slug = tmp_slug
    return slug


def validate_timezone_date(data, field, add_field=True):
    if field in data:
        value = datetime.datetime.strptime(data['field'], "%m/%d/%Y %H:%M:%S")
        data[field] = str(timezone.localtime(value))
    elif add_field:
        data[field] = str(timezone.now())
    return data