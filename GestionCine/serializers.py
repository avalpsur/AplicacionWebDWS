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
        

class ClienteSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Cliente
        fields = ['dni','nombre','apellidos','email']
        
    def validate_dni(self,dni):
        clienteDni = Cliente.objects.filter(dni=dni).first()
        if clienteDni:
            raise serializers.ValidationError("Ya existe un cliente con ese DNI")
        return dni
    
    def validate_email(self,email):
        clienteEmail = Cliente.objects.filter(email=email).first()
        if clienteEmail:
            raise serializers.ValidationError("Ya existe un cliente con ese email")
        return email

    def validate_nombre(self,nombre):
        if len(nombre) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        return nombre
    