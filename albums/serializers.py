import pytz
import datetime
from rest_framework import serializers
from django.utils import timezone
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from alsevatec.settings import TIME_ZONE
from albums.models import Album, ArtistGroup, ArtistGroupType
from albums.utils import slug_generator, validate_timezone_date


class DateTimeFieldWihTZ(serializers.DateTimeField):
    '''Class to make output of a DateTime Field timezone aware
    '''
    def to_representation(self, value):
        from_zone = pytz.timezone(TIME_ZONE)
        value = value.astimezone(from_zone)
        return super(DateTimeFieldWihTZ, self).to_representation(value)

class ArtistGroupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistGroupType
        fields = ('id', 'name', 'slug')

class ArtistGroupSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    type = ArtistGroupTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ArtistGroupType.objects.filter(active=True),
                                                   source='type', required=True)
    created_at = DateTimeFieldWihTZ()
    updated_at = DateTimeFieldWihTZ()

    class Meta:
        model = ArtistGroup
        fields = ('id', 'name', 'type', 'type_id', 'albums', 'slug', 'created_at', 'updated_at', 'active')
        extra_kwargs = {
            'slug': {'read_only': True},
            'albums': {'read_only': True},
            'type': {'read_only': True}
        }

    def get_albums(self, instance):
        albums = instance.albums.all()
        serializer = AlbumWithoutArtistSerializer(albums, many=True, context=self.context)

        return serializer.data

    def create(self, validated_data):
        model = Album
        name = validated_data['name']
        validated_data['slug'] = slug_generator(name, model)
        from_zone = pytz.timezone(TIME_ZONE)
        if not 'created_at' in validated_data:
            validated_data['created_at'] = timezone.now()
        else:
            validated_data['created_at'] = validated_data['created_at'].astimezone(from_zone)
        if not 'updated_at' in validated_data:
            validated_data['updated_at'] = timezone.now()
        else:
            validated_data['updated_at'] = validated_data['updated_at'].astimezone(from_zone)

        obj = ArtistGroup.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        if 'name' in validated_data:
            model = Album
            name = validated_data['name']
            validated_data['slug'] = slug_generator(name, model)
        from_zone = pytz.timezone(TIME_ZONE)
        if not 'created_at' in validated_data:
            validated_data['created_at'] = instance.created_at
        else:
            validated_data['created_at'] = validated_data['created_at'].astimezone(from_zone)
        if not 'updated_at' in validated_data:
            validated_data['updated_at'] = timezone.now()
        else:
            validated_data['updated_at'] = validated_data['updated_at'].astimezone(from_zone)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance


class ArtistGroupWithoutAlbumsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtistGroup
        fields = ('id', 'name', 'type', 'slug', 'created_at', 'updated_at', 'active')


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistGroupWithoutAlbumsSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ArtistGroup.objects.filter(active=True), source='artist',required=True)

    created_at = DateTimeFieldWihTZ()
    updated_at = DateTimeFieldWihTZ()

    class Meta:
        model = Album
        fields = ('id', 'name', 'artist', 'artist_id', 'ntracks', 'year', 'slug', 'created_at', 'updated_at', 'active')
        extra_kwargs = {
            'slug': {'read_only': True}
        }

    def create(self, validated_data):
        model = Album
        name = validated_data['name']
        validated_data['slug'] = slug_generator(name, model)
        if not 'created_at' in validated_data:
            validated_data['created_at'] = timezone.now()
        else:
            validated_data['created_at'] = timezone.localtime(validated_data['created_at'], timezone=TIME_ZONE)
        if not 'updated_at' in validated_data:
            validated_data['updated_at'] = timezone.now()
        else:
            validated_data['updated_at'] = timezone.localtime(validated_data['updated_at'], timezone=TIME_ZONE)
        obj = model.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        if 'name' in validated_data:
            model = Album
            name = validated_data['name']
            validated_data['slug'] = slug_generator(name, model)
        if not 'created_at' in validated_data:
            validated_data['created_at'] = instance.created_at
        else:
            validated_data['created_at'] = timezone.localtime(validated_data['created_at'], timezone=TIME_ZONE)
        if not 'updated_at' in validated_data:
            validated_data['updated_at'] = timezone.now()
        else:
            validated_data['updated_at'] = timezone.localtime(validated_data['updated_at'], timezone=TIME_ZONE)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance

class AlbumWithoutArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ('id', 'name', 'slug', 'ntracks', 'year', 'created_at', 'updated_at', 'active')