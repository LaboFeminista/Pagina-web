from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from core.models.Usuaria import Usuaria


class UsuariaModelTest(TestCase):

    def test_creacion_y_actualizacion_de_usuario(self):
        # 1. Definimos una fecha de alta manual (por ejemplo, el 1 de Enero de 2026)
        fecha_manual_alta = timezone.make_aware(datetime(2026, 1, 1, 12, 0, 0))

        # 2. CREAMOS EL OBJETO (Simulamos el INSERT)
        usuaria = Usuaria.objects.create(
            alias="Tester",
            usuaria="test@prueba.com",
            contrasena="password123",
            fecha_alta=fecha_manual_alta,  # La pasamos manualmente
        )



        # Volvemos a traer el usuario desde la base de datos para asegurarnos del cambio
        usuaria_actualizada = Usuaria.objects.get(id=usuaria.id)
        # usuaria = Usuaria.objects.get(id=usuaria)

        
        print(f"\n✅ Prueba superada con éxito:")
        print(f"   Fecha Alta (Manual): {usuaria_actualizada.fecha_alta}")
        print(f"   Fecha Conexión Nueva (Auto): {usuaria_actualizada.fecha_ultima_conexion}")
        print(f"   Usuaria actualizada: {usuaria_actualizada} ")