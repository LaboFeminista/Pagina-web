from django.db import models


class Usuaria(models.Model):
    # Django creará el campo 'id' (Primary Key) automáticamente aquí debajo.

    # Alias: string con máximo 10 caracteres
    alias = models.CharField(max_length=10, unique=True)

    usuaria = models.CharField()
    
    # Contraseña: string de máximo 9 caracteres (Ver nota de seguridad abajo ⚠️)
    password = models.CharField(max_length=9)
    
    # Fecha de última conexión: tipo date (permite estar vacío si nunca se ha conectado)
    fecha_ultima_conexion = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # Activo: tipo boolean (por defecto inicia en True)
    activo = models.BooleanField(default=True)
    
    # Fecha de alta: tipo date (se graba automáticamente la fecha del día de creación)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    
    # Fecha de baja: tipo date (puede ser nulo hasta que el usuario se dé de baja)
    fecha_baja = models.DateTimeField(null=True)

    def __str__(self):
        return self.alias
    
    class Meta:
        db_table = 'usuarias'
