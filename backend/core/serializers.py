from rest_framework import serializers
from .models import Producto  # Cambia 'TuModelo' por el tuyo

class TuModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__' # Esto expone todos los campos del modelo