from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection, transaction
from .models import *

def index(request):
    try:
        if request.method =='GET':
            context = {
                "productos" : listarProductos()
            }
            return render(request, 'index.html', context)
        if  request.method =='POST':
            usuarios = Usuario.objects.all()
            correo=request.POST['email']
            password=request.POST['password']
            for usuario in usuarios:
                if usuario.correo_usuario==correo and usuario.contrasenia_usuario==password:                
                    request.session['user']=correo
                    context = {
                    "productos" : listarProductos()
                    }
                    return redirect('index')
            empleados = Empleado.objects.all()
            for empleado in empleados:
                if empleado.correo_empleado==correo and empleado.contrasenia_empleado==password:            
                    return redirect("https://adminappdigital.herokuapp.com/?user="+correo+"")

            context = {
                "productos" : listarProductos(),
                "message" : "Usuario o contraseña erroneo"
            }
        return render(request, 'index.html', context)
    except Exception as e:
        respuesta=str(e)
        return redirect('respuesta',{'respuesta' : respuesta})

def respuesta(request):
    return render (request, 'respuesta.html')

def registro(request):
    if request.method =='GET':  
        comunas = Comuna.objects.all()
        context = {
        "comunas" : comunas
         }
        return render(request, 'registro.html', context)
    if request.method =='POST':  
        try: 
            nombres_usuario = request.POST['nombres']    
            apellidos_usuario = request.POST['apellidos']
            rut = request.POST['rut']
            direccion_usuario = request.POST['direccion']
            comuna_usuario = Comuna.objects.get(id_comuna=request.POST['comuna'])
            correo = request.POST['email']
            contrasenia = request.POST['password']
            tipoUsuario= TipoUsuario.objects.get(id_tipo_usuario=1)
            
            user = Usuario(rut_usuario=rut, nombre_usuario=nombres_usuario, apellido_usuario=apellidos_usuario, direccion=direccion_usuario, id_comuna= comuna_usuario, correo_usuario=correo, contrasenia_usuario=contrasenia, tipo_usuario=tipoUsuario, activo='1')
            user.save()
            
            comunas = Comuna.objects.all()
            print('Hola')
            context = {
            "message" : "Usuario registrado correctamente",
            "comunas" : comunas
            }
            return render(request, 'registro.html', context)
        except:
            comunas = Comuna.objects.all()
            context = {
            "message" : "Usuario no registrado, por favor intente nuevamente",
            "comunas" : comunas
            }
            return render(request, 'registro.html', context)

def desconectar(request):
    if 'user' in request.session:
        del request.session['user']
        context = {
            "productos" : listarProductos()
        }
        return render(request, 'index.html', context)
    else:
        context = {
            "productos" : listarProductos()
        }
        return render(request, 'index.html', context)

def contacto(request):
    return render(request, 'contact.html')

def productos(request):
    context = {
        "productos" : listarProductos()
    }
    return render(request, 'productos.html', context)

def detail(request):
    codigo=request.GET.get("id")
    context = {
        "producto" : buscarProducto(codigo)
    }
    return render(request, 'detail.html', context)

def buscardorDeProductos(request):
    entrada=request.POST['entrada']
    context = {
        "productos" : buscardorProductos(entrada)
    }
    return render(request, 'productos.html', context)

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

def agregarCarroCompra(request):
    codigo=request.GET.get("id")
    agregarProductoCarro(buscarProducto(codigo), request)
    return redirect('carro')

def eliminarCarroCompra(request):
    codigo=request.GET.get("id")
    eliminarProductoCarro(buscarProducto(codigo), request)
    return redirec

def finalizarVenta(request):
    if request.method =='GET': 
        context = {
            "medioPago" : MedioPago.objects.all()
        }
        return render(request, 'finalizarCompra.html', context)
    if request.method =='POST':
        medioPago = request.POST["medioPago"]
        despacho = request.POST["despacho"]
        user=request.session['user']
        if despacho is '1':
            usuarios = Usuario.objects.all()
            tipoPrecios = TipoPrecio.objects.all()
            tp=''
            for usuario in usuarios:
                if user == usuario.correo_usuario:
                    user = usuario.rut_usuario 

            for productos in request.session["carroCompra"]:
                for tipoPrecio in tipoPrecios:
                    if productos[0][8] == tipoPrecio.nombre_tipo_precio:
                        tp = tipoPrecio.id_tipo_precio

                finalizarVentaLocal(user , productos[0][0], 1, medioPago, tp)

            del request.session["carroCompra"]
            del request.session["cantCarroCompra"]
            del request.session["totalCarro"]
            return render(request, 'index.html')
        if despacho is '0':
            request.session["medioPago"]=medioPago
            return redirect('despacho')

def misCompras(request):
    return render(request, 'misCompras.html')

def comprasConEnvio(request):
    user=request.session['user']
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        if user == usuario.correo_usuario:
            user = usuario.rut_usuario 
    print(listarComprasConEnvio(user))
    context = {
        "compras" : listarComprasConEnvio(user),
        "tipo" : 1
    }
    return render(request, 'compras.html', context)

def comprasSinEnvio(request):
    user=request.session['user']
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        if user == usuario.correo_usuario:
            user = usuario.rut_usuario 
            
    context = {
        "compras" : listarComprasSinEnvio(user),
        "tipo" : 0
    }
    return render(request, 'compras.html', context)

def despacho(request):
    if request.method =='GET':
        context = {
            "PrecioDespacho" : PrecioDespacho.objects.all()
        }
        return render(request, 'despacho.html', context)
    if request.method =='POST':
        idDespacho = request.POST["PrecioDespacho"]
        direccion = request.POST["direccion"]
        detalle = request.POST["detalle"]
        medioPago = request.session["medioPago"]
        user=request.session['user']

        usuarios = Usuario.objects.all()
        tipoPrecios = TipoPrecio.objects.all()
        tp=''
        for usuario in usuarios:
            if user == usuario.correo_usuario:
                user = usuario.rut_usuario 

        for productos in request.session["carroCompra"]:
            for tipoPrecio in tipoPrecios:
                if productos[0][8] == tipoPrecio.nombre_tipo_precio:
                    tp = tipoPrecio.id_tipo_precio

            finalizarVentaEnvio(user, productos[0][0], 1, medioPago, tp, idDespacho, direccion, detalle)
        
        del request.session["carroCompra"]
        del request.session["cantCarroCompra"]
        del request.session["totalCarro"]
        return redirect('index')
        

def listarProductos():
    cursor = connection.cursor()
    cursor.execute("CALL heroku_b5f4bd0f80d05ae.ListarProducto")
    productos = cursor.fetchall()
    cursor.close()
    return productos

def listarComprasSinEnvio(rut):
    cursor = connection.cursor()
    cursor.execute("CALL heroku_b5f4bd0f80d05ae.BuscarVentaSinEnvio("+"'"+rut+"'"+")")
    ventas = cursor.fetchall() 
    cursor.close()
    return ventas

def listarComprasConEnvio(rut):
    cursor = connection.cursor()
    cursor.execute("CALL heroku_b5f4bd0f80d05ae.BuscarVentaEnvio("+"'"+rut+"'"+")")
    ventas = cursor.fetchall() 
    cursor.close()
    return ventas

def buscarProducto(codigo):
    cursor = connection.cursor()
    cursor.execute("CALL heroku_b5f4bd0f80d05ae.BuscarProducto("+codigo+")")
    producto = cursor.fetchall()
    cursor.close()
    return producto

def buscardorProductos(entrada):
    cursor = connection.cursor()
    cursor.execute('CALL heroku_b5f4bd0f80d05ae.BuscarProductoCI('+"'"+entrada+"'"+')')
    productos = cursor.fetchall()
    cursor.close()
    return productos

def finalizarVentaLocal(rut, codigo, unidades, medioPago, tipoPrecio):
    cursor = connection.cursor()
    cursor.execute('CALL heroku_b5f4bd0f80d05ae.AgregarVenta('+"'"+rut+"'"+','+str(codigo)+','+str(unidades)+','+str(medioPago)+','+str(tipoPrecio)+')')
    cursor.close()

def finalizarVentaEnvio(rut, codigo, unidades, medioPago, tipoPrecio, idDespacho, direccion, detalle):
    cursor = connection.cursor()
    cursor.execute('CALL heroku_b5f4bd0f80d05ae.AgregarVentaEnvio('+"'"+rut+"'"+','+str(codigo)+','+str(unidades)+','+str(medioPago)+','+str(tipoPrecio)+','+str(idDespacho)+','+"'"+direccion+"'"+','+"'"+detalle+"'"+')')
    cursor.close()

def agregarProductoCarro(producto, request):
    if 'carroCompra' in request.session and 'cantCarroCompra' in request.session and 'totalCarro' in request.session: 
        print(producto)
        carroCompra = request.session["carroCompra"]
        cantCarroCompra = request.session["cantCarroCompra"]
        totalCarro = request.session["totalCarro"]
        totalCarro = totalCarro + producto[0][7]
        carroCompra.append(producto)
        cantCarroCompra += 1
        request.session["carroCompra"] = carroCompra
        request.session["cantCarroCompra"] = cantCarroCompra
        request.session["totalCarro"] = totalCarro
    else:
        carroCompra = []
        cantCarroCompra = []
        totalCarro = producto[0][7]
        carroCompra.append(producto)
        cantCarroCompra = 1
        request.session["carroCompra"] = carroCompra
        request.session["cantCarroCompra"] = cantCarroCompra
        request.session["totalCarro"] = totalCarro

def eliminarProductoCarro(producto, request):
    carroCompra = request.session["carroCompra"]
    cantCarroCompra = request.session["cantCarroCompra"]
    totalCarro = request.session["totalCarro"]
    totalCarro = totalCarro - producto[0][7] 
    i=0
    for productos in carroCompra:
        if  productos[0][0] == producto[0][0]:
            carroCompra.pop(i)
                
        i += 1
    cantCarroCompra -= 1
    request.session["carroCompra"] = carroCompra
    request.session["cantCarroCompra"] = cantCarroCompra
    request.session["totalCarro"] = totalCarro
