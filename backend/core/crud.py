from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models.Usuaria import Usuaria

def crear_usuaria(alias, usuaria, password, activo=True):
    """
    Crea un registro de Usuaria en la BD.
    """
    alias_limpio = alias.strip().lower()
    datos = {
        "alias": alias_limpio,
        "usuaria": usuaria,
        "password": password,
    }
    if "activo" in [field.name for field in Usuaria._meta.get_fields()]:
        datos["activo"] = activo
    return Usuaria.objects.create(**datos)

def obtener_todos_los_usuarias():
    return Usuaria.objects.all()

def obtener_usuaria_por_id(usuaria_id):
    return get_object_or_404(Usuaria, id=usuaria_id)

def actualizar_usuaria(usuaria_id, datos_a_actualizar):
    usuaria = obtener_usuaria_por_id(usuaria_id)
    campos_validos = {field.name for field in Usuaria._meta.get_fields() if hasattr(field, 'name')}
    for campo, valor in datos_a_actualizar.items():
        if campo in campos_validos and campo != "fecha_alta":
            setattr(usuaria, campo, valor)
    usuaria.save()
    return usuaria

def eliminar_usuaria_fisico(usuaria_id):
    usuaria = obtener_usuaria_por_id(usuaria_id)
    usuaria.delete()
    return True

def eliminar_usuaria_logico(usuaria_id):
    usuaria = obtener_usuaria_por_id(usuaria_id)
    if "activo" in {field.name for field in Usuaria._meta.get_fields()}:
        usuaria.activo = False
    if "fecha_baja" in {field.name for field in Usuaria._meta.get_fields()}:
        usuaria.fecha_baja = timezone.now().date()
    usuaria.save()
    return usuaria