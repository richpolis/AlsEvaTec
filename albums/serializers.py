import pytz
import datetime
from rest_framework import serializers
from django.utils import timezone
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from alsevatec.settings import TIME_ZONE
from albums.models import Album, ArtistGroup, ArtistGroupType
from albums.utils import slug_generator, validate_timezone_date


class ArtistGroupSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    otype_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ArtistGroupType.objects.filter(active=True),
                                                   source='otype', required=True)

    class Meta:
        model = ArtistGroup
        fields = ('id', 'name', 'otype', 'otype_id', 'albums', 'slug', 'created_at', 'updated_at', 'active')
        extra_kwargs = {
            'slug': {'read_only': True},
            'albums': {'read_only': True},
            'otype': {'read_only': True}
        }

    def get_albums(self, instance):
        albums = Album.objects.filter(artist=instance)
        serializer = AlbumWithoutArtistSerializer(albums, many=True, context=self.context)

        return serializer.data

    # def validate(self, attrs):
    #     user_time_zone = pytz.timezone(TIME_ZONE)
    #     if 'created_at' in attrs:
    #         created_at = datetime.datetime.strptime(attrs['created_at'], "%m/%d/%Y %H:%M:%S")
    #         attrs['created_at'] = str(user_time_zone.localize(created_at))
    #     if 'updated_at' in attrs:
    #         created_at = datetime.datetime.strptime(attrs['updated_at'], "%m/%d/%Y %H:%M:%S")
    #         attrs['updated_at'] = str(timezone.localtime(created_at))
    #     return attrs

    def create(self, validated_data):
        model = Album
        name = validated_data['name']
        validated_data['slug'] = slug_generator(name, model)
        #validated_data = validate_timezone_date(validated_data, 'created_at')
        #validated_data = validate_timezone_date(validated_data, 'updated_at')

        obj = ArtistGroup.objects.create(name=name, slug=validated_data['slug'])
        obj.created_at = timezone.now()
        obj.updated_at = timezone.now()
        obj.otype = validated_data['otype']
        obj.save()
        return obj

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        if 'name' in validated_data:
            model = Album
            name = validated_data['name']
            validated_data['slug'] = slug_generator(name, model)
        #validated_data = validate_timezone_date(validated_data, 'created_at', False)
        #validated_data = validate_timezone_date(validated_data, 'created_at', False)
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
        fields = ('id', 'name', 'otype', 'slug', 'created_at', 'updated_at', 'active')


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistGroupWithoutAlbumsSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ArtistGroup.objects.filter(active=True), source='artist',required=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'artist', 'artist_id', 'slug', 'created_at', 'updated_at', 'active')
        extra_kwargs = {
            'slug': {'read_only': True},
        }

    # def validate(self, attrs):
    #     uuser_time_zone = pytz.timezone(TIME_ZONE)
    #     if 'created_at' in attrs:
    #         created_at = datetime.datetime.strptime(attrs['created_at'], "%m/%d/%Y %H:%M:%S")
    #         attrs['created_at'] = str(user_time_zone.localize(created_at))
    #     if 'updated_at' in attrs:
    #         created_at = datetime.datetime.strptime(attrs['updated_at'], "%m/%d/%Y %H:%M:%S")
    #         attrs['updated_at'] = str(timezone.localtime(created_at))
    #     return attrs

    def create(self, validated_data):
        model = Album
        name = validated_data['name']
        validated_data['slug'] = slug_generator(name, model)
        #validated_data = validate_timezone_date(validated_data, 'created_at')
        #validated_data = validate_timezone_date(validated_data, 'updated_at')

        obj = model.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        if 'name' in validated_data:
            model = Album
            name = validated_data['name']
            validated_data['slug'] = slug_generator(name, model)
        #validated_data = validate_timezone_date(validated_data, 'created_at', False)
        #validated_data = validate_timezone_date(validated_data, 'created_at', False)
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
        fields = ('id', 'name', 'slug', 'created_at', 'updated_at', 'active')