# apps/usuarios/crud.py
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models.usuaria import Usuaria

# ==========================================
# 1. CREATE (Crear Usuario)
# ==========================================
def crear_usuaria(alias, usuaria,contrasena, activo):
    """
    Toma los datos limpios del front y hace un INSERT en la base de datos.
    """
    # El ORM se encarga de crear el objeto y asignarle un ID automático
    nuevo_usuaria = Usuaria(
        alias=alias.strip().lower(),
        contrasena=contrasena
    )
    nuevo_usuaria.save() # Guarda físicamente en la BD
    return nuevo_usuaria


# ==========================================
# 2. READ (Leer / Consultar usuarias)
# ==========================================
def obtener_todos_los_usuarias():
    """
    Hace un SELECT * de todos los usuarias de la base de datos.
    """
    return usuaria.objects.all()

def obtener_usuaria_por_id(usuaria_id):
    """
    Hace un SELECT con un WHERE id = usuaria_id. 
    Si no existe, levanta un error 404 de forma segura.
    """
    return get_object_or_404(usuaria, id=usuaria_id)


# ==========================================
# 3. UPDATE (Actualizar usuaria)
# ==========================================
def actualizar_usuaria(usuaria_id, datos_a_actualizar):
    """
    Busca al usuaria por ID y actualiza solo los campos que envíe el front.
    'datos_a_actualizar' es un diccionario, ej: {"alias": "nuevo_nick", "activo": False}
    """
    usuaria = obtener_usuaria_por_id(usuaria_id)
    
    # Recorremos los datos que envió el front y los asignamos al objeto
    for campo, valor in datos_a_actualizar.items():
        # Evitamos modificar campos internos como la fecha de alta
        if hasattr(usuaria, campo) and campo != 'fecha_alta':
            setattr(usuaria, campo, valor)
            
    usuaria.save() # Ejecuta el UPDATE en la base de datos
    return usuaria


# ==========================================
# 4. DELETE (Borrar Usuario)
# ==========================================
def eliminar_usuario_fisico(usuario_id):
    """
    Borrado Físico: Elimina el registro por completo de la base de datos (DELETE).
    """
    usuario = obtener_usuario_por_id(usuario_id)
    usuario.delete() # Borra de la BD
    return True

def eliminar_usuario_logico(usuario_id):
    """
    Borrado Lógico (Recomendado para APIs): No borra los datos, 
    solo desactiva al usuario y le pone fecha de baja.
    """
    usuario = obtener_usuario_por_id(usuario_id)
    usuario.activo = False
    usuario.fecha_baja = timezone.now().date()
    usuario.save() # Guarda los cambios del estado
    return usuario