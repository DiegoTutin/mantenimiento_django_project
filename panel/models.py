from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MaxLengthValidator,
)
class Clientes(models.Model):
    id = models.IntegerField(primary_key=True)
    nombres = models.CharField(max_length=30, null=False)
    apellidos = models.CharField(max_length=30, null=False)
    tipo_identificacion = models.CharField(max_length=20, null=False)
    numero_identificacion = models.CharField(max_length=40, null=False)
    correo_electronico = models.CharField(max_length=30, null=False)
    celular = models.CharField(max_length=20, null=False)
    direccion = models.CharField(max_length=50, null=False)


class Meta:
    db_table = "clientes"


class Tipo_equipos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    codigo = models.CharField(max_length=30, null=False)
    estado_respaldo = models.BooleanField(default=False)


class Meta:
    db_table = "tipo_equipos"

class Accesorio(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = "accesorios"

    def __str__(self):
        return self.nombre
    
    
class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = "estados"

    def __str__(self):
        return self.nombre

class Ordenes_Mantenimiento(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Tipo_equipos, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    
    numero_serie = models.CharField(max_length=50, null=True, blank=True)
    estado_equipo = models.CharField(max_length=100, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    marca = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    contrasena = models.CharField(max_length=50, null=True, blank=True)
    
    accesorios = models.ManyToManyField(Accesorio, blank=True)
    estado = models.ManyToManyField(Estado, blank=True)  
    desea_respaldo = models.BooleanField(default=False)
    observaciones = models.TextField(null=True, blank=True)
    detalles_dano = models.TextField(null=True, blank=True)
    
    trabajo = models.IntegerField(
        null=False,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1),
            MaxLengthValidator(3),
        ],
    )

    class Meta:
        db_table = "ordenes_mantenimiento"

class MisOrdenes(models.Model):
    orden_mantenimiento = models.ForeignKey(Ordenes_Mantenimiento, on_delete=models.CASCADE)

    diagnostico = models.TextField(null=True, blank=True)
    fecha_diagnostico = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        db_table = "mis_ordenes"

    def __str__(self):
        return f"Diagnóstico para Orden #{self.orden_mantenimiento.id}"

@receiver(pre_save, sender=Ordenes_Mantenimiento)
def calcular_fecha_entrega(sender, instance, **kwargs):
    # Obtener la fecha actual
    fecha_actual = timezone.now().date()
    # Encontrar el próximo día hábil
    dias_a_sumar = 2
    for _ in range(dias_a_sumar):
        fecha_actual += datetime.timedelta(days=1)
        while fecha_actual.weekday() in [5, 6]:  # Sábado o domingo
            fecha_actual += datetime.timedelta(days=1)

    # Asignar la fecha de entrega calculada
    instance.fecha_entrega = datetime.datetime.combine(
        fecha_actual, datetime.time(8, 0)
    )  
