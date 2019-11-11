import cx_Oracle
from django.db import connection, transaction
from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
import cx_Oracle
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from faskApp.models import Trabajador, Empresa, Tarea, SubTarea
from faskApp.forms import(
TrabajadorForm, EmpresaForm,
RegistroForm, FormularioLogin, UserTrabajadorForm,UserEmpresaForm,
TareaForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

#notificacion
from django.shortcuts import render_to_response
# from django.http import HttpResponse
from faskApp.models import Notificacion

##
from django.utils.decorators import method_decorator
from .decorators import empresa_required, trabajador_required
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()


def handler500(request):
    return render(request, 'Base/error_pages/error_404.html', status=500)


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'Base/error_pages/error_404.html', data)

def home(request):
    return render(request, 'Base/index.html')

@login_required
def index(request):
	user = request.user
	if user.is_empresa:
		return redirect(reverse('faskApp:index_empresa'))
	elif user.is_trabajador:
		return redirect(reverse('faskApp:index_trabajador'))
	elif user.is_staff:
		return redirect(reverse('faskApp:index_administrador'))
	else:
		return render(request, template_name='/Base/index.html')

def index_administrador(request):
	empresa = Empresa.objects.all().order_by('id')
	contexto = {'empresa':empresa}
	n = Notificacion.objects.filter(usuario=request.user, visto = False)
	return render(request, 'admin_pages/index.html', {'notificaciones': n,'empresa':empresa})


def index_empresa(request):
	n = Notificacion.objects.filter(usuario=request.user, visto = False)
	return render(request, 'empresa_pages/index.html', {'notificaciones': n})


def index_trabajador(request):
	n = Notificacion.objects.filter(usuario=request.user, visto = False)
	print(request.user.id)
	trab_id = Trabajador.objects.get(user_id = request.user.id)
	tarea = Tarea.objects.filter(trabajador_id=trab_id, estado = True).order_by('id')   
	contexto = {'tarea':tarea}
	print(trab_id)
	return render(request, 'trabajador_pages/index.html', {'notificaciones': n, 'tarea':tarea})

# region LOGIN-LOGOUT-PASWORD

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView


class Login(FormView):
    template_name = 'registration/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('home1')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)
		

def logouts(request):
        logout(request)
        return HttpResponseRedirect('/')
# endregion


# region Trabajador
class TrabajadorList(ListView):
	model = Trabajador
	template_name = 'empresa_pages/lista_trabajadores.html'


class TrabajadorCreate(CreateView):
	model = Trabajador
	template_name = 'empresa_pages/agregar_trabajador.html'
	form_class = TrabajadorForm
	second_form_class = UserTrabajadorForm 
	success_url = reverse_lazy('faskApp:listar_trabajadores')

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'trabajador'
		context = super(TrabajadorCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			xd = Empresa.objects.get(user_id = request.user.id)
			trabajador = form.save(commit=False)
			trabajador.empresa = xd
			trabajador.user = form2.save()			
			trabajador.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

# @method_decorator([login_required, trabajador_required], name='dispatch')
class TrabajadorUpdate(UpdateView):
	model = Trabajador
	second_model = User
	template_name = 'empresa_pages/agregar_trabajador.html'
	form_class = TrabajadorForm
	second_form_class = UserTrabajadorForm 
	success_url = reverse_lazy('faskApp:listar_trabajadores')


	def get_context_data(self, **kwargs):
	    context = super(TrabajadorUpdate, self).get_context_data(**kwargs)
	    pk = self.kwargs.get('pk', 0)
	    trabajador = self.model.objects.get(id=pk)
	    persona = self.second_model.objects.get(id=trabajador.user_id)
	    if 'form' not in context:
	    	context['form'] = self.form_class()
	    if 'form2' not in context:
	    	context['form2'] = self.second_form_class(instance=persona)
	    context['id'] = pk
	    return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_trabajador = kwargs['pk']
		trabajador = self.model.objects.get(id=id_trabajador)
		persona = self.second_model.objects.get(id=trabajador.user_id)
		form = self.form_class(request.POST, instance=trabajador)
		form2 = self.second_form_class(request.POST, instance=persona)
		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class TrabajadorDelete(DeleteView):
	model = Trabajador
	template_name = 'empresa_pages/eliminar_trabajador.html'
	success_url = reverse_lazy('faskApp:listar_trabajadores')

# endregion

# region Empresa
def perfilEmpresa(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'empresa_pages/perfil_empresa.html', args)

class EmpresaList(ListView):
	model = Empresa
	template_name = 'admin_pages/listar_empresa.html'

class AdminEmpresaIndex(ListView):
	model = Empresa
	template_name = 'admin_pages/index.html'


class EmpresaCreate(CreateView):
	model = Empresa
	template_name = 'admin_pages/agregar_empresa.html'
	form_class = EmpresaForm
	second_form_class = UserEmpresaForm 
	success_url = reverse_lazy('faskApp:listar_empresa')

	def get_context_data(self, **kwargs):
		context = super(EmpresaCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			empresa = form.save(commit=False)
			empresa.user = form2.save()
			empresa.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class EmpresaUpdate(UpdateView):
	model = Empresa
	second_model = User
	template_name = 'admin_pages/agregar_empresa.html'
	form_class = EmpresaForm
	second_form_class = UserEmpresaForm 
	success_url = reverse_lazy('faskApp:listar_empresa')


	def get_context_data(self, **kwargs):
	    context = super(EmpresaUpdate, self).get_context_data(**kwargs)
	    pk = self.kwargs.get('pk', 0)
	    empresa = self.model.objects.get(id=pk)
	    persona = self.second_model.objects.get(id=empresa.user_id)
	    if 'form' not in context:
	    	context['form'] = self.form_class()
	    if 'form2' not in context:
	    	context['form2'] = self.second_form_class(instance=persona)
	    context['id'] = pk
	    return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_empresa = kwargs['pk']
		empresa = self.model.objects.get(id=id_empresa)
		persona = self.second_model.objects.get(id=empresa.user_id)
		form = self.form_class(request.POST, instance=empresa)
		form2 = self.second_form_class(request.POST, instance=persona)
		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())


class EmpresaDelete(DeleteView):
	model = Empresa
	template_name = 'admin_pages/eliminar_empresa.html'
	success_url = reverse_lazy('faskApp:listar_empresa')
# endregion

#region Tarea
class TreaList(ListView):
	model = Tarea
	template_name = 'trabajador_pages/index.html'
	

class TreaCreate(CreateView):
	model = Tarea
	template_name = 'empresa_pages/Tarea/crear_tarea.html'
	form_class = TareaForm
	success_url = reverse_lazy('faskApp:index_empresa')

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form_class = self.form_class(request.POST)	
		if form_class.is_valid():
			print("sdfsdfsdf")
			xd = Empresa.objects.get(user_id = request.user.id)
			tarea = form_class.save(commit=False)
			tarea.estado = True
			tarea.empresa = xd
			trabajador = request.POST['trabajador']
			titulo = request.POST['titulo']
			Book.createusuario=kwargs.get('instance'),titulo ="Nueva tarea ",comentario = "gracias por iniciar secion")
			book = Notificacion(title=title)
			tarea.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form_class))



class TreaUpdate(UpdateView):
	model = Empresa
	second_model = User
	template_name = 'admin_pages/agregar_empresa.html'
	form_class = EmpresaForm
	second_form_class = UserEmpresaForm 
	success_url = reverse_lazy('faskApp:listar_empresa')



class TreaDelete(DeleteView):
	model = Empresa
	template_name = 'admin_pages/eliminar_empresa.html'
	success_url = reverse_lazy('faskApp:listar_empresa')
#endregion



#regions notificaciones
@login_required
def mostrarNotificacionEmpresa(request, pk):
	user = request.user
	n = Notificacion.objects.get(id=pk)
	if user.is_empresa:
		return render(request,'empresa_pages/notificacion_empresa.html',{'notificaciones':n})
	elif user.is_trabajador:
		return render(request,'trabajador_pages/notificacion_trabajador.html',{'notificaciones':n})
	elif user.is_staff:
		return render(request,'empresa_pages/notificacion_empresa.html',{'notificaciones':n})
	else:
		return render(request,'empresa_pages/notificacion_empresa.html',{'notificaciones':n})
	# return render(request,'empresa_pages/notificacion_empresa.html',{'notificaciones':n})

@login_required
def eliminarNotificacionEmpresa(request, pk):
	n = Notificacion.objects.get(id=pk)
	user = request.user
	n.visto = True
	n.save()
	if user.is_empresa:
		return HttpResponseRedirect(reverse('faskApp:index_empresa'))
	elif user.is_trabajador:
		return HttpResponseRedirect(reverse('faskApp:index_trabajador'))
	elif user.is_staff:
		return HttpResponseRedirect(reverse('faskApp:index_admin'))
	else:
		return HttpResponseRedirect(reverse('/'))
	

# @login_required
# def mostrarNotificacionTrabajador(request, pk):
# 	n = Notificacion.objects.get(id=pk)
# 	return render(request,'empresa_pages/notificacion_empresa.html',{'notificaciones':n})
# 	# return render(request,'empresa_pages/notificacion_empresa.html',{'notificaciones':n})

# @login_required
# def eliminarNotificacionTrabajador(request, pk):
# 	n = Notificacion.objects.get(id=pk)
# 	n.visto = True
# 	n.save()
# 	return HttpResponseRedirect(reverse('faskApp:index_empresa'))

#endregion


def buscarProducto(request):
	codigo=123456789
	context = {"producto": listarProductos(codigo)}
	# prints(context)
	# print(buscarProducto(codigo))
	return render(request, 'SELECT.html', context)


def listarProductos(codigo):
	cursor = connection.cursor()
	l_cur = cursor.var(cx_Oracle.CURSOR).var
	print(l_cur)
	# cursor.execute("CALL heroku_b5f4bd0f80d05ae.ListarProducto")
	l_emp = cursor.callproc("PKG_HR.FIND_EMPLOYEES")
	# print(cursor.stored_results())
	l_cur.getvalue()
	print("SS")
	print(l_cur.getvalue())
	print("22")
	return list(l_emp)
	# productos = cursor.fetchall()
	# cursor.close()
	# return productos


#  def find_employees(self, p_query):
#      # as it comes to all complex types we need to tell Oracle Client
#      # what type to expect from an OUT parameter
# 	l_cur = self.__cursor.var(cx_Oracle.CURSOR)
# 	l_query, l_emp = self.__cursor.callproc("PKG_HR.FIND_EMPLOYEES", [p_query, l_cur])
# 	return list(l_emp)



#region admin

def detalle_empresa(request,id):
	codigo= Empresa.objects.get(id=id)
	print(codigo.id)
	numero = codigo.id
	print(listartrabajador(numero))
	context = {
		"cont_trabajadores" : listartrabajador(numero)
	}
	return render(request, 'select.html', context)



def listartrabajador(codigo):
    cursor = connection.cursor()
	# SELECT COUNT(trabajador.id) from trabajador where empresa_id=101
    cursor.execute(" SELECT COUNT(trabajador.id) from trabajador where empresa_id="+str(codigo)+"")
    ventas = cursor.fetchall()
    cursor.close()
    return ventas

#endregion