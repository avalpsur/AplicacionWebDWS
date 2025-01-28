from rest_framework import serializers
from .models import *

        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
        
class CineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cine
        fields = '__all__'
        
class SalaSerializer(serializers.ModelSerializer):
    cine = CineSerializer(read_only=True, many=False)
    class Meta:
        model = Sala
        fields = '__all__'
        
class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'
        
        
class PeliculaSerializerMejorado(serializers.ModelSerializer):
    sala = SalaSerializer(read_only=True, many=True)
    class Meta:
        model = Pelicula
        fields = '__all__'
        