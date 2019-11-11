from django.db import models
from django.contrib.auth.models import AbstractUser
from bootstrap_datepicker_plus import DateTimePickerInput
# from django.contrib.auth.models import User

#notifications
from django.db.models.signals import post_save
from django.dispatch import receiver
# from faskApp.models import Tarea
# Create your models here.
class User(AbstractUser):
    is_empresa = models.BooleanField(default=False)
    is_trabajador = models.BooleanField(default=False)



class Empresa(models.Model):
    rut = models.IntegerField('rut',  blank = False, null = False)
    nombre = models.CharField('Nombre', max_length=150, blank = False, null = False)
    # correo = models.EmailField('Correo', max_length=255, blank = False, null = False)
    telefono = models.CharField('Telefono', max_length=10, blank = False, null = False)
    fecha_creacion =models.DateField("Fecha de creacion", auto_now=True, auto_now_add=False)
    fecha_modificacion =models.DateField("Fecha de modificacion",blank = True,null = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_empre",null=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']
        db_table = 'empresa'

    def __str__(self):
        return self.nombre


class Trabajador(models.Model):
    rut = models.IntegerField('Rut',  blank = False, null = False)
    nombre = models.CharField('Nombre', max_length=150, blank = False, null = False)
    apellidoP = models.CharField('Apellido paterno', max_length=150, blank = False, null = False)
    apellidoM= models.CharField('Apellido materno', max_length=150, blank = False, null = False)
    # correo = models.EmailField('Correo', max_length=255, blank = False, null = False)
    celular = models.IntegerField('Celular',  blank = False, null = False)
    telefono = models.IntegerField('Telefono', blank = True, null = True)
    fecha_creacion =models.DateField("Fecha de creacion", auto_now=True, auto_now_add=False)
    fecha_modificacion =models.DateField("Fecha de modificacion",blank = True,null = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_trab",null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="empresa_trab",blank = True,null=True)
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['fecha_creacion']
        db_table = 'trabajador'

    def __str__(self):
        return self.nombre




class Tarea(models.Model):
    titulo = models.CharField('Comentario',max_length=255,  blank = False, null = False)
    comentario = models.CharField('Comentario',max_length=255,  blank = False, null = False)
    fecha_vencimiento = models.DateField("Fecha de vencimiento",blank = True,null = True)
    estado = models.BooleanField('Estado', null = False)   
    fecha_creacion =models.DateField("Fecha de creacion", auto_now=True, auto_now_add=False)
    fecha_modificacion =models.DateField("Fecha de modificacion",blank = True,null = True)
    trabajador = models.ForeignKey (Trabajador,  on_delete=models.CASCADE, related_name="trabajador",null=True)
    depende = models.ForeignKey('self', on_delete=models.CASCADE, related_name="gg",null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="empresa",null=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['id']
        db_table = 'tarea'

    # def __str__(self):
    #     return self.titulo


# @receiver(post_save,sender=Tarea)
# def create_tarea_menssage(sender, **kwargs):
#     if kwargs.get('created',False):
#         Notificacion.objects.create(
#         usuario=kwargs.get('instance'),
#         titulo ="Nueva Tarea ",
#         comentario = " Tienes una nueva tarea"
#         )
    



class SubTarea(models.Model):
    subtarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, blank = False, null = False)
    comentario = models.CharField('Comentario', max_length=255, blank = False, null = False)
    estado = models.BooleanField('Estado', blank = False, null = False)  
    fecha_creacion =models.DateField("Fecha de creacion", auto_now=True, auto_now_add=False)
    fecha_modificacion =models.DateField("Fecha de modificacion",blank = True,null = True)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="tarea",null=True)

    class Meta:
        verbose_name = 'Sub tarea'
        verbose_name_plural = 'Sub tareas'
        ordering = ['fecha_creacion']
        db_table = 'sub_tarea'

    def __str__(self):
        return self.fecha_creacion
    







#notifications
class Notificacion(models.Model):
    titulo = models.CharField('Titulio',max_length=255,  blank = False, null = False)
    comentario = models.CharField('Comentario',max_length=255,  blank = False, null = False)
    visto = models.BooleanField(' Visto', default = False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'notificacion'





@receiver(post_save,sender=User)
def create_welcome_menssage(sender, **kwargs):
    if kwargs.get('created',False):
        Notificacion.objects.create(usuario=kwargs.get('instance'),
        titulo ="bienvenido ",
        comentario = "gracias por iniciar secion"
        )

