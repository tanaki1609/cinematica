from rest_framework import serializers
from .models import Film


class FilmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = 'id title release_year'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
