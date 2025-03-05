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

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'



class SalaSerializer(serializers.ModelSerializer):
    cine = CineSerializer(read_only=True)  # Anida los detalles de Cine
    empleado = EmpleadoSerializer(many=True, read_only=True)  # Anida los detalles de Empleado
    
    class Meta:
        model = Sala
        fields = ['id', 'tamano', 'cine', 'empleado']

class SalaSerializerEditar(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['tamano', 'cine', 'empleado']

class SalaSerializerActualizarTamano(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['tamano']

from rest_framework import serializers
from .models import *

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
    
class SalaSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['tamano', 'cine', 'empleado']

    def validate_tamano(self, tamano):
        opciones_validas = ["PE", "ME", "GR"]
        if tamano not in opciones_validas:
            raise serializers.ValidationError("El tamaño debe ser 'PE' (Pequeño), 'ME' (Mediano) o 'GR' (Grande).")
        return tamano

    def validate_cine(self, cine):
        if not Cine.objects.filter(id=cine.id).exists():
            raise serializers.ValidationError("El cine seleccionado no existe.")
        return cine

    def validate_empleado(self, empleados):
        if not empleados:
            raise serializers.ValidationError("Debes asignar al menos un empleado a la sala.")
        return empleados

class PeliculaSerializerEditar(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ['nombre', 'descripcion', 'fecha_estreno', 'sala']

class PeliculaSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ['nombre']

class PeliculaSerializerCreate(serializers.Serializer):
    titulo = serializers.CharField(max_length=500)
    director = serializers.CharField(max_length=300)
    sinopsis = serializers.CharField(required=False, allow_blank=True)
    fechaLanzamiento = serializers.DateField()
    tiempoProyectada = serializers.DurationField(required=False, allow_null=True)
    sala = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    def validate_titulo(self, titulo):
        if len(titulo) < 3:
            raise serializers.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo

    def validate_director(self, director):
        if len(director) < 3:
            raise serializers.ValidationError("El nombre del director debe tener al menos 3 caracteres.")
        return director

    def validate_fechaLanzamiento(self, fechaLanzamiento):
        if fechaLanzamiento > timezone.now().date():
            raise serializers.ValidationError("La fecha de lanzamiento no puede ser en el futuro.")
        return fechaLanzamiento

    def validate_sala(self, salas):
        if not salas:
            raise serializers.ValidationError("Debes seleccionar al menos una sala.")
        
        for sala_id in salas:
            if not Sala.objects.filter(id=sala_id).exists():
                raise serializers.ValidationError(f"La sala con ID {sala_id} no existe.")
        
        return salas

    def create(self, validated_data):
        salas_data = validated_data.pop('sala')
        pelicula = Pelicula.objects.create(**validated_data)
        pelicula.sala.set(salas_data)
        pelicula.save()
        return pelicula

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.director = validated_data.get('director', instance.director)
        instance.sinopsis = validated_data.get('sinopsis', instance.sinopsis)
        instance.fechaLanzamiento = validated_data.get('fechaLanzamiento', instance.fechaLanzamiento)
        instance.tiempoProyectada = validated_data.get('tiempoProyectada', instance.tiempoProyectada)
        
        if 'sala' in validated_data:
            salas_data = validated_data.pop('sala')
            instance.sala.set(salas_data)
        
        instance.save()
        return instance
    
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username