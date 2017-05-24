#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#Guillermo Labrador Vázquez
#Parseamos el documento XML de aparcamientos

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

def normalize_whitespace(text):
    #Con esta funcion, pasamos de tener dos espacios a tener uno.
    return string.join(string.split(text), ' ')


class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inContent = False
        self.theContent = ""
        self.atributo = ""
        self.accesible = False
        """self.nombre = ""
        self.descripcion = ""
        self.accesibilidad = ""
        self.url = ""
        self.nombre_via = ""
        self.clase_vial = ""
        self.num = ""
        self.codigo_postal = ""
        self.barrio = ""
        self.distrito = ""
        self.latitud = ""
        self.longitud = ""
        self.telefono = ""
        self.email = """""
        self.i = 0
        self.aparcamiento = {} #informacion de un aparcamiento.
        self.lista_aparcamientos = [] #formado por una lista de todos los aparcamientos.
        self.lista_aparcamientos_otra = []

    def startElement (self, name, attrs):
        if name == 'atributo':
            self.atributo = attrs.get("nombre")
        if self.atributo in ["NOMBRE", "DESCRIPCION", "ACCESIBILIDAD", "CONTENT-URL", "NOMBRE-VIA", "CLASE-VIAL", "NUM", "CODIGO-POSTAL", "BARRIO", "DISTRITO", "LATITUD", "LONGITUD", "TELEFONO", "EMAIL"]:
            self.inContent = True


    def endElement (self, name):

        if self.atributo == "NOMBRE":

            #self.nombre = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "DESCRIPCION":

            #self.descripcion = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "ACCESIBILIDAD":

            #self.accesibilidad = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            if self.theContent == "1":
                self.accesible = True
            self.i += 1

        elif self.atributo == "CONTENT-URL":

            #self.url = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "NOMBRE-VIA":

            #self.nombre_via = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "CLASE-VIAL":

            #self.clase_vial = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "NUM":

            #self.num = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "CODIGO-POSTAL":

            #self.codigo_postal = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "BARRIO":

            #self.barrio = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "DISTRITO":

            #self.distrito = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "LATITUD":

            #self.latitud = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "LONGITUD":

            #self.longitud = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "TELEFONO":

            #self.telefono = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1

        elif self.atributo == "EMAIL":

            #self.email = self.theContent
            self.aparcamiento[self.atributo] = self.theContent
            self.i += 1


        #if self.inContent:
            #print(self.aparcamiento) #algo ocurre con el self.aparcamiento
            #self.lista_aparcamientos.append(self.aparcamiento)

        if name == "contenido":
            self.lista_aparcamientos.append(self.aparcamiento)
            self.aparcamiento = {}
            self.i = 0

        if name == "contenido" and self.accesible == True:
            self.lista_aparcamientos_otra.append(self.aparcamiento)

        self.inContent = False
        self.theContent = ""


    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

    def returnParkingList (self):
        #print(self.lista_aparcamientos)
        return self.lista_aparcamientos

    def returnAccesibleParkingList(self):

        return self.lista_aparcamientos_otra
# Load parser and driver

"""theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = urllib.request.urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
theParser.parse(xmlFile)"""

#print ("Parse complete")
