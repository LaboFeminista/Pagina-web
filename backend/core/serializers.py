# apps/usuarios/serializers.py
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Campos que expondremos en la API
        fields = ['id', 'alias', 'contrasena', 'activo', 'fecha_alta']
        # El ID y la fecha de alta los maneja el servidor, el cliente no puede enviarlos
        read_only_fields = ['id', 'fecha_alta']
        # Hacemos que la contraseña sea solo de escritura (para que nunca viaje en los GET)
        extra_kwargs = {
            'contrasena': {'write_only': True}
        }

    # =========================================================
    # PASO 1: INTERCEPTAR Y LIMPIAR (Antes de validar)
    # =========================================================
    def to_internal_value(self, data):
        datos_limpios = data.copy()
        
        # Quitamos espacios molestos en los extremos y pasamos el alias a minúsculas
        if 'alias' in datos_limpios and isinstance(datos_limpios['alias'], str):
            datos_limpios['alias'] = datos_limpios['alias'].strip().lower()
            
        if 'contrasena' in datos_limpios and isinstance(datos_limpios['contrasena'], str):
            datos_limpios['contrasena'] = datos_limpios['contrasena'].strip()
            
        return super().to_internal_value(datos_limpios)

    # =========================================================
    # PASO 2: VALIDACIÓN DE CAMPOS INDIVIDUALES
    # =========================================================
    
    def validate_alias(self, value):
        # El modelo ya valida el máximo de 10 caracteres, aquí añadimos lógica de negocio
        if " " in value:
            raise serializers.ValidationError("El alias no puede contener espacios intermedios.")
        
        # Bloquear nombres de usuario reservados del sistema
        nombres_prohibidos = ['admin', 'root', 'api', 'password']
        if value in nombres_prohibidos:
            raise serializers.ValidationError(f"El alias '{value}' está reservado por el sistema.")
            
        return value

    def validate_contrasena(self, value):
        # Validar largo mínimo (el máximo de 9 ya lo frena el modelo automáticamente)
        if len(value) < 6:
            raise serializers.ValidationError("La contraseña debe tener entre 6 y 9 caracteres.")
            
        # Forzar a que tenga al menos una letra y un número
        tiene_letra = any(char.isalpha() for char in value)
        tiene_numero = any(char.isdigit() for char in value)
        
        if not tiene_letra or not tiene_numero:
            raise serializers.ValidationError("La contraseña debe ser alfanumérica (combinar letras y números).")
            
        return value

    # =========================================================
    # PASO 3: VALIDACIÓN GENERAL/CRUZADA (Múltiples campos)
    # =========================================================
    def validate(self, attrs):
        """
        Este método corre al final. 'attrs' ya contiene los datos que pasaron 
        las validaciones individuales de arriba.
        """
        alias = attrs.get('alias')
        contrasena = attrs.get('contrasena')

        # Regla de seguridad: La contraseña no puede ser igual al alias
        if alias and contrasena and alias == contrasena.lower():
            raise serializers.ValidationError({
                "contrasena": "Por seguridad, tu contraseña no puede ser idéntica a tu alias."
            })

        return attrs