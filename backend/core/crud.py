# apps/usuarios/crud.py
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Usuario

# ==========================================
# 1. CREATE (Crear Usuario)
# ==========================================
def crear_usuario(alias, contrasena):
    """
    Toma los datos limpios del front y hace un INSERT en la base de datos.
    """
    # El ORM se encarga de crear el objeto y asignarle un ID automático
    nuevo_usuario = Usuario(
        alias=alias.strip().lower(),
        contrasena=contrasena
    )
    nuevo_usuario.save() # Guarda físicamente en la BD
    return nuevo_usuario


# ==========================================
# 2. READ (Leer / Consultar Usuarios)
# ==========================================
def obtener_todos_los_usuarios():
    """
    Hace un SELECT * de todos los usuarios de la base de datos.
    """
    return Usuario.objects.all()

def obtener_usuario_por_id(usuario_id):
    """
    Hace un SELECT con un WHERE id = usuario_id. 
    Si no existe, levanta un error 404 de forma segura.
    """
    return get_object_or_404(Usuario, id=usuario_id)


# ==========================================
# 3. UPDATE (Actualizar Usuario)
# ==========================================
def actualizar_usuario(usuario_id, datos_a_actualizar):
    """
    Busca al usuario por ID y actualiza solo los campos que envíe el front.
    'datos_a_actualizar' es un diccionario, ej: {"alias": "nuevo_nick", "activo": False}
    """
    usuario = obtener_usuario_por_id(usuario_id)
    
    # Recorremos los datos que envió el front y los asignamos al objeto
    for campo, valor in datos_a_actualizar.items():
        # Evitamos modificar campos internos como la fecha de alta
        if hasattr(usuario, campo) and campo != 'fecha_alta':
            setattr(usuario, campo, valor)
            
    usuario.save() # Ejecuta el UPDATE en la base de datos
    return usuario


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