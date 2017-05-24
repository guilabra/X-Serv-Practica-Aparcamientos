from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from myfinalapp.models import Aparcamiento, Comentario, CSS, Aparcamiento_Seleccionado
from operator import itemgetter
import urllib.request
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from myfinalapp.xml_parser import myContentHandler
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@csrf_exempt
def start(request):

    lista = []
    lista_usuarios = []
    all_parkings = Aparcamiento.objects.all()

    #Si el numero de aparcamientos no esta cargado, parseamos y guardamos la lista en la base de datos
    if len(all_parkings) < 1:
        theParser = make_parser()
        theHandler = myContentHandler()
        theParser.setContentHandler(theHandler)

        #Obtengo la lista de los aparcamientos
        xmlFile = urllib.request.urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
        theParser.parse(xmlFile)
        lista = theHandler.returnParkingList()

        #Guardo la lista en la base de datos
        saveDic(lista)
        all_parkings = Aparcamiento.objects.all()

    #Ordenamos el diccionario por el numero de comentarios, que se nos pide en la pagina principal.
    ordered_all_parkings = orderComments(all_parkings)
    #print(ordered_all_parkings)
    lista_aparcamientos = []
    counter = 5 #Quiero que me muestre 5 aparcamientos
    #el ordered_all_parkings nos devuelve el id y el numero de comentarios.
    for argument in ordered_all_parkings:

        if counter > 0 and argument[1]!=0 :
            counter -= 1
            try:
                #Cogemos el id del aparcamiento
                aparcamiento = Aparcamiento.objects.get(id = argument[0])
                usuarios = User.objects.all()
                for usuario in usuarios:
                    try:
                        css = CSS.objects.get(usuario = usuario.username)
                        if len(lista_usuarios) < len(usuarios):
                            lista_usuarios.append((css.usuario, css.titulo))
                    except CSS.DoesNotExist:
                        if len(lista_usuarios) < len(usuarios):
                            lista_usuarios.append((usuario.username, "Página de " + usuario.username))

                lista_aparcamientos.append(aparcamiento)
            except ObjectDoesNotExist:
                print("Ese aparcamiento no existe")

    template = get_template('plantilla_base.html')
    #context = RequestContext(request, )
    return HttpResponse(template.render({'aparcamientos': lista_aparcamientos, 'usuarios': lista_usuarios}, request))

@csrf_exempt
def saveDic(lista):
    for dic_aparcamiento in lista:
        nombre = dic_aparcamiento['NOMBRE']
        try:
            descripcion = dic_aparcamiento['DESCRIPCION']
        except KeyError:
            descripcion = "---"
        accesibilidad = dic_aparcamiento['ACCESIBILIDAD']
        url = dic_aparcamiento['CONTENT-URL']
        try:
            c_postal = dic_aparcamiento['CODIGO-POSTAL']
        except KeyError:
            c_postal = "---"
        try:
            num = dic_aparcamiento['NUM']
        except KeyError:
            num = "---"
        direccion = dic_aparcamiento['NOMBRE-VIA'] + ", " + num + ", " + c_postal
        try:
            barrio = dic_aparcamiento['BARRIO']
        except KeyError:
            barrio = "---"
        try:
            distrito = dic_aparcamiento['DISTRITO']
        except KeyError:
            distrito = "---"
        try:
            latitud = dic_aparcamiento['LATITUD']
        except KeyError:
            latitud = "---"
        try:
            longitud = dic_aparcamiento['LONGITUD']
        except KeyError:
            longitud = "---"
        coordenadas = latitud + ", " + longitud
        try:
            telefono = dic_aparcamiento['TELEFONO']
        except KeyError:
            telefono = "---"
        try:
            email = dic_aparcamiento['EMAIL']
        except KeyError:
            email = "---"
        contacto = telefono + ", " + email
        parking = Aparcamiento(nombre = nombre, accesibilidad = accesibilidad, url = url, direccion = direccion, barrio = barrio, distrito = distrito, coordenadas = coordenadas, contacto = contacto, descripcion = descripcion)
        parking.save()

@csrf_exempt
def orderComments(lista):
    dic = {}
    lista_ordenada = []
    for aparcamiento in lista:
        id = aparcamiento.id
        try:
            comentarios = Comentario.objects.filter(aparcamiento_id = id)
            dic[id] = len(comentarios) #carga el numero de comentarios por cada parking, que tiene asociado un id.
        except Comentarios.DoesNotExist:
            print("No hay comentarios")

    lista_ordenada = sorted(dic.items(), key = itemgetter(1), reverse = True)
    return lista_ordenada

@csrf_exempt
def showParkings(request):
    aparcamientos = Aparcamiento.objects.all()
    #print(aparcamientos)
    template = get_template('plantilla_aparcamientos.html')

    return HttpResponse(template.render({'aparcamientos': aparcamientos}, request))

@csrf_exempt
def filtParkings(request):
    lista_aparcamientos = []
    distrito = request.POST.get("distrito")
    todos = Aparcamiento.objects.all()
    if distrito == "todos":
        lista_aparcamientos = Alojamiento.objects.all()
    else:
        lista_aparcamientos = Aparcamiento.objects.filter(distrito=distrito)

    template = get_template('plantilla_aparcamientos.html')

    return HttpResponse(template.render({'aparcamientos': lista_aparcamientos, 'todos': todos}, request))

@csrf_exempt
def showParkingId(request, id):
    try:
        aparcamiento = Aparcamiento.objects.get(id=id)
        comentarios = Comentario.objects.filter(aparcamiento_id=aparcamiento)
        if len(comentarios)==0:
            comentarios = []
    except ObjectDoesNotExist:
        print ("No existe el aparcamiento con ese identificador")
    template = get_template('plantilla_aparcamientoid.html')
    return HttpResponse(template.render({'aparcamiento': aparcamiento, 'comentarios': comentarios}, request))

@csrf_exempt
def showAbout(request):
    template = get_template('plantilla_about.html')
    return HttpResponse(template.render(request))

@csrf_exempt
def tolog(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
    return HttpResponseRedirect("/")

@csrf_exempt
def userPage(request, username):
    lista_aparcamientos = []
    #username = request.user.username
    try:
        css = CSS.objects.get(usuario=username)
        titulo = css.titulo
        u = username
        usuario = User.objects.get(username=username)
    except CSS.DoesNotExist:
        usuario = User.objects.get(username=username)
        u = usuario.username
        titulo = ""
    try:
        aparcamientos_seleccionados = Aparcamiento_Seleccionado.objects.filter(usuario=usuario)
        for aparcamiento in aparcamientos_seleccionados:

            lista_aparcamientos.append((aparcamiento))
    except ObjectDoesNotExist:
            print ("No hay aparcamientos seleccionados")
    template = get_template('plantilla_usuario.html')
    return HttpResponse(template.render({'aparcamientos': lista_aparcamientos, 'usuario': u, 'titulo': titulo}, request))

@csrf_exempt
def includeComment(request, identif):
    if request.user.is_authenticated():
        comentario = request.POST.get("comentario")
        aparcamiento = Aparcamiento.objects.get(id=identif)
        nuevo = Comentario(aparcamiento_id=aparcamiento, comentario=comentario)
        nuevo.save()
        return HttpResponseRedirect("/aparcamientos/" + str(identif))
    else:
        return HttpResponseRedirect("/aparcamientos/" + str(identif))

@csrf_exempt
def includeFavorite(request, identif):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            usr = User.objects.get(username=username)
            aparcamiento = Aparcamiento.objects.get(id=identif)
            comentarios = Comentario.objects.filter(aparcamiento_id=aparcamiento)
            if len(comentarios)==0:
                comentarios = []
            try:
                Aparcamiento_Seleccionado.objects.get(aparcamiento_id=aparcamiento)
                template = get_template('plantilla_aparcamientoid_solicitado.html')
                return HttpResponse(template.render({'aparcamiento': aparcamiento, 'comentarios': comentarios}, request))
            except Aparcamiento_Seleccionado.DoesNotExist:
                favorito = Aparcamiento_Seleccionado(aparcamiento_id=aparcamiento, usuario=usr)
                favorito.save()
                template = get_template('plantilla_aparcamientoid.html')
                return HttpResponse(template.render({'aparcamiento': aparcamiento, 'comentarios': comentarios}, request))
        except ObjectDoesNotExist:
            print ("No existe el aparcamiento solicitado")

@csrf_exempt
def changeTitle(request):
    lista_aparcamientos = []
    if request.user.is_authenticated():
        username = request.user.username
        titulo = request.POST.get("titulo")
        try:
            css = CSS.objects.get(usuario=username)
            css.titulo = titulo
            css.save()
            usuario = User.objects.get(username=username)
        except CSS.DoesNotExist:
            css = CSS(usuario=username, titulo=titulo)
            css.save()
            usuario = User.objects.get(username=username)
    else:
        titulo = ""
        usuario = User.objects.get(username=request.user.username)
        username = usuario.username
    try:
        aparcamientos_seleccionados = Aparcamiento_Seleccionado.objects.filter(usuario=usuario)
        for aparcamiento in aparcamientos_seleccionados:

            lista_aparcamientos.append((aparcamiento))

    except ObjectDoesNotExist:
            print ("No existen favoritos...")
    template = get_template('plantilla_usuario.html')
    return HttpResponse(template.render({'aparcamientos': lista_aparcamientos, 'usuario': username, 'titulo': titulo}, request))


@csrf_exempt
def showXML(request, username):
    aparcamientos_seleccionados = []

    try:
        username = User.objects.get(username = username)
    except ObjectDoesNotExist:
        return HttpResponse("404 Not Found. No estas loggeado")

    seleccionados = Aparcamiento_Seleccionado.objects.filter(usuario = username)
    for seleccionado in seleccionados:
        aparcamientos_seleccionados.append(seleccionado)

    template = get_template('plantilla_xml.xml')
    context = {'seleccionados': aparcamientos_seleccionados}

    return HttpResponse(template.render(context, request), content_type = 'text/xml')
