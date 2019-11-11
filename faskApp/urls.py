from django.contrib import admin
from django.urls import path
from faskApp.views import ( 
logouts,Login,
index_empresa,index_administrador,index_trabajador,
TrabajadorList,TrabajadorCreate,TrabajadorUpdate,TrabajadorDelete,
EmpresaList,EmpresaCreate,EmpresaUpdate,EmpresaDelete,perfilEmpresa,
TreaCreate,TreaList,
AdminEmpresaIndex,
mostrarNotificacionEmpresa,eliminarNotificacionEmpresa,
detalle_empresa,

)

app_name = 'faskApp'
urlpatterns = [
    #URL LOGINS ETC
    path('logout/', logouts, name='logout'),
    path("login/", Login.as_view(), name="login"),
    #URLS AMINISTRADOR
    path('administrador/', index_administrador, name='index_administrador'),
    path('administrador/listar_empresa/',  EmpresaList.as_view(),name='listar_empresa'),
    path('administrador/agregar_empresa/',  EmpresaCreate.as_view(),name='agregar_empresa'),
    path('administrador/editar_empresa/<int:pk>/',  EmpresaUpdate.as_view(),name='editar_empresa'),
    path('administrador/eliminar_empresa/<int:pk>/',  EmpresaDelete.as_view(),name='eliminar_empresa'),
    path('administrador/detalle_empresa/<int:id>/', detalle_empresa, name='detalle_empresa'),


    #URLS TRABAJADOR
    path('trabajador/',index_trabajador,name='index_trabajador'),

    # path('trabajador/',TreaList.as_view(),name='index_trabajador'),
    #URL EMPRESA
    path('perfilempresa/',  perfilEmpresa,name='perfil_empresa'),
    path('empresa/',  index_empresa,name='index_empresa'),
    path('empresa/listar_trabajador/',  TrabajadorList.as_view(),name='listar_trabajadores'),
    path('empresa/agregar_trabajador/',  TrabajadorCreate.as_view(),name='agregar_trabajador'),
    path('empresa/editar_trabajador/<int:pk>/',  TrabajadorUpdate.as_view(),name='editar_trabajador'),
    path('empresa/eliminar_trabajador/<int:pk>/',  TrabajadorDelete.as_view(),name='eliminar_trabajador'),
    path('empresa/crear_tarea/', TreaCreate.as_view(), name='crear_tarea'),
    #notificaciones
    path('empresa/notificacion/show/<int:pk>/',mostrarNotificacionEmpresa , name='show_notif'),
    path('empresa/notificacion/delete/<int:pk>/', eliminarNotificacionEmpresa , name='delete_notif'),
] 
