from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as rest_framework_response
from albums.models import Album, ArtistGroup
from albums.serializers import AlbumSerializer, ArtistGroupSerializer


class AlbumsGenericMixin(object):
    model_class = None

    def get_model(self):
        return self.model_class

    def return_response(self, data={}, message='', extra='Ningun problema', status=200):
        data = {
            "code": status,
            "data": data,
            "msj": {message},
            "extra": {extra}
        }
        return rest_framework_response(data, status=status)


class AlbumsCreateModelMixin(viewsets.mixins.CreateModelMixin):
    model_text_created = 'Registro creado'
    model_text_not_created = 'Registro no creado'

    def create(self, request, *args, **kwargs):
        try:
            serializer_model_class = self.get_serializer_class()
            serializer = serializer_model_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, self.model_text_created)
        except Exception as e:
            return self.return_response(message=self.model_text_not_created, extra=e.args.__str__(),
                                        status=status.HTTP_400_BAD_REQUEST)


class AlbumsUpdateModelMixin(viewsets.mixins.UpdateModelMixin):
    model_text_updated = 'Registro actualizado'
    model_text_not_updated = 'Registro no actualizado'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer_model_class = self.get_serializer_class()
            serializer = serializer_model_class(instance, data=request.data, context={'request': request},
                                                partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, self.model_text_updated)
        except Exception as e:
            return self.return_response(message=self.model_text_not_updated, extra=e.args.__str__(),
                                        status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            instance = get_object_or_404(self.get_model(), pk=pk)
            serializer_model_class = self.get_serializer_class()
            serializer = serializer_model_class(instance, data=request.data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.return_response(serializer.data, self.model_text_updated)
        except Exception as e:
            return self.return_response(message=self.model_text_not_updated, extra=e.args.__str__(),
                                        status=status.HTTP_400_BAD_REQUEST)


class AlbumsListModelMixin(viewsets.mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return self.return_response(serializer.data, 'Registros')
        except Exception as e:
            return self.return_response(message='Registros', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)


class AlbumsRetrieveModelMixin(viewsets.mixins.RetrieveModelMixin):
    def retrieve(self, request, pk=None):
        try:
            instance = get_object_or_404(self.get_model(), pk=pk)
            serializer = self.get_serializer(instance)
            return self.return_response(serializer.data, 'Registro')
        except Exception as e:
            return self.return_response(message='Registro', extra=e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)


class AlbumsDestroyModelMixin(viewsets.mixins.DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return self.return_response(message='Registro eliminado', status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return self.return_response(message='Registro no eliminado', extra=e.args.__str__(),
                                        status=status.HTTP_400_BAD_REQUEST)


class AlbumsModelViewSet(AlbumsCreateModelMixin,
                         AlbumsRetrieveModelMixin,
                         AlbumsUpdateModelMixin,
                         AlbumsDestroyModelMixin,
                         AlbumsListModelMixin,
                         viewsets.GenericViewSet):
    """
    Generics Mixins
    """
    pass


class AlbumViewSet(AlbumsGenericMixin, AlbumsModelViewSet):
    queryset = Album.objects.filter(active=True)
    serializer_class = AlbumSerializer
    permission_classes = (AllowAny,)
    model_class = Album

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


class ArtistGroupViewSet(AlbumsGenericMixin, AlbumsModelViewSet):
    queryset = ArtistGroup.objects.filter(active=True)
    serializer_class = ArtistGroupSerializer
    permission_classes = (AllowAny,)
    model_class = ArtistGroup

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
