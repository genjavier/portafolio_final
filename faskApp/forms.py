from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from faskApp.models import Trabajador, Empresa ,Tarea
from django.contrib.auth import get_user_model
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'



class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control m-input'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control  m-login__form-input--last'
        self.fields['password'].widget.attrs['placeholder'] = 'Clave'



class RegistroForm(UserCreationForm):
		
	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control m-input'
		self.fields['password1'].widget.attrs['class'] = 'form-control  m-login__form-input--last'
		self.fields['password2'].widget.attrs['class'] = 'form-control  m-login__form-input--last'

		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None



class UserTrabajadorForm(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = User
	
	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_trabajador = True
		if commit:
			user.save()
		return user


class TrabajadorForm(forms.ModelForm):

	class Meta:
		model = Trabajador
		fields = [
			'rut',
			'nombre',
			'apellidoP',
			'apellidoM',
			# 'correo',
			'celular',
            'telefono',
            
		]
		labels = {
			'rut': 'Rut',
			'nombre': 'Nombre',
			'apellidoP' : 'Apellido paterno',
			'apellidoM' : 'Apellido materno',
			# 'correo' : 'Correo',
			'celular': 'Celular',
            'telefono':'Telefono',
          
		}
		widgets = {
			'rut':forms.NumberInput(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'apellidoP':forms.TextInput(attrs={'class':'form-control'}),
			'apellidoM':forms.TextInput(attrs={'class':'form-control'}),
			# 'correo':forms.TextInput(attrs={'class':'form-control'}),
			'celular':forms.NumberInput(attrs={'class':'form-control'}),
			'telefono':forms.NumberInput(attrs={'class':'form-control'}),
            'empresa':forms.HiddenInput(attrs={'class':'form-control'}),
		}

class UserEmpresaForm(UserCreationForm):
	email = forms.EmailField(required=True, label='Email')
	class Meta(UserCreationForm.Meta):
		model = User
	
	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_empresa = True
		if commit:
			user.save()
		return user



class EmpresaForm(forms.ModelForm):

	class Meta:
		model = Empresa
		fields = [
			'rut',
			'nombre',
			# 'correo',
                    'telefono',

		]
		labels = {
			'rut': 'Rut',
			'nombre': 'Nombre',
			# 'correo': 'Correo',
                    'telefono': 'Telefono',
		}
		widgets = {
			'rut': forms.NumberInput(attrs={'class': 'form-control'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control'}),
			# 'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),

		}

class TareaForm(forms.ModelForm):
	# fecha_vencimiento = forms.DateField(widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'type':'date', 'class':'form-control', 
                            #    'placeholder':'mas q las paloma'}))
	class Meta:
		model = Tarea
		fields = [
			'titulo',
			'comentario',
			# 'fecha_vencimiento',
			# 'fecha_creacion',
			# 'fecha_modificacion',
			'trabajador',
		]
	

		labels = {
			'titulo': 'Titulo',
			'comentario': 'Descripcion',
			# 'fecha_vencimiento' : 'fecha_vencimiento',
			'estado' : 'Estado',
			'trabajador': 'Trabajador'
			# 'fecha_creacion' : 'Fecha de creacion',
		}

	widgets = {
			'titulo': forms.TextInput(attrs={'class': 'form-control'}),
			'comentario': forms.Textarea(attrs={'class': 'form-control'}),
			# 'fecha_vencimiento':  forms.DateInput(attrs={'class':'datepicker'}),
			'estado': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
			'trabajador': forms.Select(attrs={'class': 'form-control'}),

		}