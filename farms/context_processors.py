from django.conf import settings


def mapbox_token(request):
    return {'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN}
