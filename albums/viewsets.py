from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as rest_framework_response
from albums.models import Album, ArtistGroup
from albums.serializers import AlbumSerializer, ArtistGroupSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.filter(active=True)
    serializer_class = AlbumSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        album = self.request.query_params.get('album', None)
        artist = self.request.query_params.get('artist', None)
        if album or artist:
            filters = dict()
            if artist:
                filters['artist__name__icontains'] = artist
            if album:
                filters['name__icontains'] = album
            return Album.objects.filter(**filters)
        else:
            return Album.objects.all().order_by('-id')


    def get_model(self):
        return Album

    def return_response(self, data={}, message='', extra='Ningun problema', status=200):
        data = {
            "code": data,
            "msj": {message},
            "extra": {extra}
        }
        return rest_framework_response(data, status=status)

    def create(self, request, *args, **kwargs):
        try:
            serializer = AlbumSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, 'Album creado')
        except Exception as e:
            return self.return_response(message='Album no creado', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = AlbumSerializer(instance, data=request.data, context={'request': request}, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, 'Album actualizado')
        except Exception as e:
            return self.return_response(message='Album no actualizado', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            instance = get_object_or_404(self.get_model(), pk=pk)
            serializer = AlbumSerializer(instance, data=request.data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, 'Album actualizado')
        except Exception as e:
            return self.return_response(message='Album no actualizado', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return self.return_response(serializer.data, 'Albums')
        except Exception as e:
            return self.return_response(message='Albums', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            instance = get_object_or_404(self.get_model(), pk=pk)
            serializer = self.get_serializer(instance)
            return self.return_response(serializer.data, 'Album')
        except Exception as e:
            return self.return_response(message='Album', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)


class ArtistGroupViewSet(viewsets.ModelViewSet):
    queryset = ArtistGroup.objects.filter(active=True)
    serializer_class = ArtistGroupSerializer
    permission_classes = (AllowAny,)

    def get_model(self):
        return ArtistGroup

    def get_queryset(self):
        album = self.request.query_params.get('album', None)
        artist = self.request.query_params.get('artist', None)
        if album or artist:
            filters = dict()
            if artist:
                filters['name__icontains'] = artist
            if album:
                filters['albums__name__icontains'] = album
            return ArtistGroup.objects.filter(**filters)
        else:
            return ArtistGroup.objects.all().order_by('-id')

    def return_response(self, data={}, message='', extra='Ningun problema', status=200):
        data = {
            "code": data,
            "msj": {message},
            "extra": {extra}
        }
        return rest_framework_response(data, status=status)

    def create(self, request, *args, **kwargs):
        try:
            serializer = ArtistGroupSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, 'ArtistGroup creado')
        except Exception as e:
            return self.return_response(message='ArtistGroup no creado', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ArtistGroupSerializer(instance, data=request.data, context={'request': request}, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, 'ArtistGroup actualizado')
        except Exception as e:
            return self.return_response(message='ArtistGroup no actualizado', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            instance = get_object_or_404(self.get_model(), pk=pk)
            serializer = ArtistGroupSerializer(instance, data=request.data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, 'ArtistGroup actualizado')
        except Exception as e:
            return self.return_response(message='ArtistGroup no actualizado', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return self.return_response(serializer.data, 'ArtistGroups')
        except Exception as e:
            return self.return_response(message='Albums', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            instance = get_object_or_404(self.get_model(), pk=pk)
            serializer = self.get_serializer(instance)
            return self.return_response(serializer.data, 'ArtistGroup')
        except Exception as e:
            return self.return_response(message='ArtistGroup', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)