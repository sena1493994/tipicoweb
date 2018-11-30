from django.shortcuts import render
import pyrebase
from django.contrib import auth
import traceback
import pytz

# Create your views here.

valor=0
comida=0
conectkey=""
'''CONFIGURACION DE FIREBASE EN LA WEB'''
config = {
    'apiKey': "AIzaSyD4rA3-ZMXJkiQwJdhQeFmYMicCe1pyfPc",
    'authDomain': "tipico-saludable-50fb7.firebaseapp.com",
    'databaseURL': "https://tipico-saludable-50fb7.firebaseio.com",
    'projectId': "tipico-saludable-50fb7",
    'storageBucket': "tipico-saludable-50fb7.appspot.com",
    'messagingSenderId': "159019297528"
  }
'''INICIALIZACION DE LA APP'''
firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()



'''AUTENTICCION EN FIREBASE DEL USUARIO'''
authe = firebase.auth()

def inicio(request):
 	
	return render(request,'inicio.html')
'''VISTA INICIAR SESION'''
def vista_login(request):
 	
	return render(request,'login.html')
'''FUNCION DE AUTENTICACION EN FIREBASE'''
def postsign(request):
	email = request.POST.get('email')
	passw = request.POST.get('password')
	try:
		user = authe.sign_in_with_email_and_password(email, passw)
	except:
		message="CONTRASEÑA O USUARIO INCORRECTO"
		return render(request,'login.html',{'mensaje':message})
	print(user['idToken'])
	session_id = user['idToken']
	request.session['uid']=str(session_id)

	return render(request,'plantillaBase.html',{'e':email})

def logout(request):
	auth.logout(request)
	return render(request,'inicio.html')

	
'''FUNCION DE REGISTRO DE PERFIL EN FIREBASE'''
def registro(request):
	return render(request,'registro.html')

def registrar(request):


	# 1- lista de perfiles

	lista = database.child("Usuario").shallow().get().val()
	lista_indices=[]
	for i in lista:
		lista_indices.append(i)
		
	lista_indices.sort(reverse=False)
	print(lista_indices)


	# 2-longitud de la lista


	longitud=len(lista_indices)
	print("longitud 1 : ",longitud)

	# 3-verificar si la lista esta vacia


	# 4-obtener el ultimo el de la lista

	x = len(lista_indices)
	print("x: ",x)
	ultimo_elemento = lista_indices[x-1]
	siguiente_elemento=(int(ultimo_elemento)+1)
	print("ultimo elemento de la lista: ",int(ultimo_elemento))
	print("siguiente elemto a crear: ",int(siguiente_elemento))



	# 5-iniciar a crear desde cero solo si lista esta vacia
	



	# 6- obtenemos los datos del formulario


	email = request.POST.get('email')
	password = request.POST.get('password')
	nombre = request.POST.get('nombre')
	imagen =request.POST.get('url3')
	rol= request.POST.get('rol')



	# 7- creamos logica para que los registros no se remplazen 

	

	lista2= database.child("Usuario").shallow().get().val()
	lista_indices2=[]
	for i in lista2:
		lista_indices2.append(i)
	
	lista_indices2.sort(reverse=False)
	print(lista_indices2)
	longitud2=len(lista_indices2)
	print("longitud 2: ",longitud2)
	if(longitud==longitud2):
		print("longitud final: ",longitud2)
		data={
			"nombre":nombre,
			"password":password,
			"email":email,
			"rol":rol,
			"imagen":imagen
		}

	
	# 8- agregamos data a la base de datos

	
	database.child("Usuario").child(str(siguiente_elemento)).set(data)
	
		


	# try:

	# 	#el child en el cual se va a agregar es Usuario
	# 	timestamps= database.child("Usuario").shallow().get().val()
	# 	list_time=[]
	# 	for i in timestamps:

	# 		list_time.append(i)
		
	# 	list_time.sort(reverse=False)
	# 	print(list_time)
	# 	valor=len(list_time)
	# 	print("valor: ",valor)

	# except:
	# 	pass
	# 	print("Hay algo raro")

	# email = request.POST.get('email')
	# passw = request.POST.get('password')
	# nombre = request.POST.get('nombre')
	# file = request.POST.get('url3')
	# rol = request.POST.get('rol') 

	# print(email,passw,nombre,file,rol)
	# try:
	# 	timestamps2= database.child("Usuario").shallow().get().val()
	# 	list_time4=[]
	# 	for i in timestamps2:

	# 		list_time4.append(i)
		
	# 	list_time.sort(reverse=False)
	# 	print(list_time4)
	# 	valor2=len(list_time4)
	# 	#obtienen el tamaño de la lista
	# 	print("valor 2: ",valor2)
	# 	#user = authe.create_user_with_email_and_password(email,passw)
	# 	if(valor==valor2):
	# 		print("valor final: ",valor)
	# 		data={
	# 			"Correo":email,
	# 			"Contrasenia":passw,
	# 			"Nombre":nombre,
	# 			"imagen":file,
	# 			"rol":rol
	# 		}
	# 	database.child("Usuario").child(str(siguiente_elemento)).set(data)

	# except:
	# 	mensaje="No se puede crear la cuenta"
	# 	return render(request,'registro.html',{'mensaje':mensaje})
	# 	#uid = user['localId']

	return render(request,'registro.html')

def vista_editar_perfil(request, idenu):

	print(idenu)

	getnombre = database.child("Usuario").child(str(idenu)).child("nombre").shallow().get().val()
	getemail = database.child("Usuario").child(str(idenu)).child("email").shallow().get().val()
	getpassw  = database.child("Usuario").child(str(idenu)).child("passw").shallow().get().val()
	getrol = database.child("Usuario").child(str(idenu)).child("rol").shallow().get().val()
	
	print(getnombre,getemail,getpassw,getrol)
	


	email = request.POST.get('email')
	passw = request.POST.get('password')
	nombre = request.POST.get('nombre')
	file = request.POST.get('url')
	rol = request.POST.get('rol') 
	print(email,passw,file,nombre,rol)

	try:

		timestamps2= database.child("Usuarios").shallow().get().val()
		
		#obtienen el tamaño de la lista
		
		data={
			"correo":email,
			"contraseña":passw,
			"nombre":nombre,
			"foto":file,
			"rol":rol
		}
		database.child("Usuarios").child().set(data)
		return render(request, 'editar_perfil.html', locals())

	except:
		mensaje="No se puede crear la cuenta"
		return render(request,'editar_perfil.html',{'mensaje':mensaje})
		#uid = user['localId']



	return render(request, 'editar_perfil.html', locals())




def lista_perfil(request):
	timestamps = database.child("Usuario").shallow().get().val()
	list_time=[]
	try:
		timestamps= database.child("Usuario").shallow().get().val()
		for i in timestamps:
			print (database.child("Usuario").get().val())
			list_time.append(i)
		

		lista = sorted (list_time)
		print(lista, "con sorted")
		print(list_time, "con sort")

		nom=[]
		
		for i in list_time:
			nombre = database.child("Usuario").child(i).child("nombre").get().val()
			nom.append(nombre)
		print(nom)

		role=[]
		for i in list_time:
			rol = database.child("Usuario").child(i).child("rol").get().val()
			role.append(rol)
		print(role)

		fot=[]
		for i in list_time:
			foto=database.child("Usuario").child(i).child("imagen").get().val()
			fot.append(foto)
			print(fot)

		correou=[]
		for i in list_time:
			correo = database.child("Usuario").child(i).child("email").get().val()
			correou.append(correo)
		print(correo)



		passwor=[]
		for i in list_time:
			passw = database.child("Usuario").child(i).child("password").get().val()
			passwor.append(passw)
		print(correo)

		paquete_list = zip(list_time,nom,role,fot,correou,passwor)

	except:
		pass
		print("problemas")
	

	return render(request, 'perfiles.html',locals())

#REGISTRO COMIDAS

def vista_registro_comida(request):
	#primero se lista los datos del nodo
	try:
		#el child en le cual se va a agregar es Comida
		timestamps= database.child("Comida").shallow().get().val()
		lista_time=[]
		for i in timestamps:

			lista_time.append(i)
		
		lista_time.sort(reverse=True)
		print(lista_time)
		valor=len(lista_time)
		#obtienen el tamaño de la lista
		print("comida: ",comida)

	except:
		pass
		print("problemas")

	nombre 			= request.POST.get('nombre')
	calorias 		= request.POST.get('calorias')
	carbohidratos 	= request.POST.get('carbohidratos')
	proteinas 		= request.POST.get('proteinas')
	iddrawable 		= request.POST.get('url')
	receta 			= request.POST.get('url1')
	print("xxxxxxxxxxxxxxxx")
	print(nombre,calorias,carbohidratos,proteinas,iddrawable,receta)
	print("xxxxxxxxxxxxxxxx")

	try:
		timestamps3= database.child("Comida").shallow().get().val()
		lista_time3=[]
		for i in timestamps3:

			lista_time3.append(i)
		
		lista_time.sort(reverse=True)
		print(lista_time3)
		comida2=len(lista_time3)
		print("comida 2: ",comida2)
		#user = authe.create_user_with_email_and_password(email,passw)

		if(comida==comida2):
			print("valor final: ",comida)
		#user = authe.create_user_with_email_and_password(email,passw)
		data= { 
				"Nombre":nombre,
				"Calorias":calorias,
				"Carbohidratos":carbohidratos,
				"Proteinas":proteinas,
				"Receta":receta,
				"idDrawable":iddrawable,
		}
		database.child("Comida").child(str(valor)).set(data)	


	except:
		mensaje="No se puede guardar los datos"
		return render(request, 'registro_comida.html',{'mensaje':mensaje},{'db': nombre})
		uid = nombre['localId']
	
	return render(request, 'registro_comida.html')

def vista_lista_comida(request):
	timestamps = database.child("Comida").shallow().get().val()
	lista_time=[]
	for i in timestamps:
		lista_time.append(i)
	lista_time.sort(reverse=True)
	print(lista_time)

	nom=[]
	for i in lista_time:
		nombre = database.child("Comida").child(i).child("Nombre").get().val()
		nom.append(nombre)
	print(nom)

	calor=[]
	for i in lista_time:
		calorias = database.child("Comida").child(i).child("Calorias").get().val()
		calor.append(calorias)
	print(calor)

	carbo=[]
	for i in lista_time:
		carbohidratos = database.child("Comida").child(i).child("Carbohidratos").get().val()
		carbo.append(carbohidratos)
	print(carbo)

	prot=[]
	for i in lista_time:
		proteinas = database.child("Comida").child(i).child("Proteinas").get().val()
		prot.append(proteinas)
	print(prot)

	foto=[]
	for i in lista_time:
		imagencomida = database.child("Comida").child(i).child("idDrawable").get().val()
		foto.append(imagencomida)
	print(foto)

	receta=[]
	for i in lista_time:
		rece = database.child("Comida").child(i).child("Receta").get().val()
		receta.append(rece)
	print(receta)

	paquete_list = zip(lista_time,foto,nom,calor,carbo,prot,receta)

	return render(request, 'lista_comida.html', locals())

#Ver eliminar

# logica de los deportes
def vista_agregar_deporte(request):


	if request.method== "POST":	

		# 1-lista deportes

		lista = database.child("Deportes").shallow().get().val()
		lista_indices=[]
		for i in lista:
			lista_indices.append(i)
			
		lista_indices.sort(reverse=False)
		print(lista_indices)

		# 2-longitud de la lista


		longitud=len(lista_indices)
		print("longitud 1 : ",longitud)

		# 3-verificar si la lista esta vacia


		# 4-obtener el ultimo el de la lista

		x = len(lista_indices)
		print("x: ",x)
		ultimo_elemento = lista_indices[x-1]
		siguiente_elemento=(int(ultimo_elemento)+1)
		print("ultimo elemento de la lista: ",int(ultimo_elemento))
		print("siguiente elemto a crear: ",int(siguiente_elemento))


		# 5-iniciar a crear desde cero solo si lista esta vacia
		




		# 6- obtenemos los datos del formulario



		nombre = request.POST.get('nombre')
		calorias = request.POST.get('calorias')
		categoria = request.POST.get('categoria')
		duracion =request.POST.get('duracion')
		imagen= request.POST.get('url')
		
		

		# 7- creamos logica para que los registros no se remplazen 

	

		lista2= database.child("Deportes").shallow().get().val()
		lista_indices2=[]
		for i in lista2:
			lista_indices2.append(i)
		
		lista_indices2.sort(reverse=False)
		print(lista_indices2)
		longitud2=len(lista_indices2)
		print("longitud 2: ",longitud2)
		if(longitud==longitud2):
			print("longitud final: ",longitud2)
			data={
				"nombre":nombre,
				"calorias":calorias,
				"categoria":categoria,
				"duracion":duracion,
				"imagen":imagen
			}

		# 8- agregamos data a la base de datos


		database.child("Deportes").child(str(siguiente_elemento)).set(data)
		mensaje="Registro exitoso"
			
		
	return render(request,'agregar_deporte.html')



def vista_listar_deporte(request):
	# idtoken= request.session['uid']
	# a= authe.get_account_info(idtoken)
	# a=a['users']
	# a=a[0]
	# a=a['localid']

	lis_time=[]

	try:
		

		timestamps= database.child("Deportes").shallow().get().val()
		for i in timestamps:

			lis_time.append(i)
		
		lis_time.sort(reverse=True)
		print(lis_time)



		nombre=[]

		for i in lis_time:
			wor = database.child("Deportes").child(i).child("nombre").get().val()
			nombre.append(wor)
		print(nombre)



		cal=[]

		for a in lis_time:
			calorias=database.child("Deportes").child(a).child("calorias").get().val()
			cal.append(calorias)
		print(cal)



		cat=[]

		for a in lis_time:
			categoria=database.child("Deportes").child(a).child("categoria").get().val()
			cat.append(categoria)
		print(cat)


		dur=[]

		for a in lis_time:
			duracion=database.child("Deportes").child(a).child("duracion").get().val()
			dur.append(duracion)
		print(dur)



		ima=[]

		for a in lis_time:
			imagen=database.child("Deportes").child(a).child("imagen").get().val()
			ima.append(imagen)
		print(ima)

		comb_lis= zip(lis_time,nombre,cal,cat,dur,ima)

	except:
		pass

	

	return render(request,'listar_deporte.html',locals())

def vista_editar_deporte(request, iden):

	print (iden)

	getnombre = database.child("Deportes").child(str(iden)).child("nombre").shallow().get().val()
	getcalorias = database.child("Deportes").child(str(iden)).child("calorias").shallow().get().val()
	getduracion = database.child("Deportes").child(str(iden)).child("duracion").shallow().get().val()
	getcategoria = database.child("Deportes").child(str(iden)).child("categoria").shallow().get().val()
	print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
	print (getnombre,getcalorias,getduracion,getcategoria)
	print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

	if request.method== "POST":	
		index = request.POST.get('index')
		nombre = request.POST.get('nombre')
		calorias = request.POST.get('calorias')
		categoria = request.POST.get('categoria')
		duracion =request.POST.get('duracion')
		imagen= request.POST.get('url')
		# print(email)
		try:
			#user = authe.create_user_with_email_and_password(email,passw)
			data={
				"nombre":nombre,
				"calorias":calorias,
				"categoria":categoria,
				"duracion":duracion,
				"imagen":imagen
			}
			#se pasa el valor del tamaño de la lista a un chlid y se hace un set a dicho child
			database.child("Deportes").child(iden).update(data)
			mensaje="Cambio exitoso"
			
			return render(request,'editar_deporte.html',locals())
		except:
			mensaje="No se puede editar el deporte"
			return render(request,'editar_deporte.html',locals())
	

	
	return render(request,'editar_deporte.html',locals())


