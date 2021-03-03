#!/usr/bin/env python3
"""
    AUTORES: RUBEN EMMANUEL GARCIA ORDAZ - GERARDO SANTOYO BORJON


"""
import time
import pickle
from os import system
from platform import system as sys
import netifaces
from os import listdir
from os.path import isfile, join
#Constantes de color utiles para la impresion de texto en consola
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[39m'
def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
def validar(strn):
    op = ""
    def saveBand():
        op = input(strn)
        return op
    if op == "S" or op == "N" or op == "s" or op == "n":
        if op == "n" or op == "N":
            return False
        else:
            return True
    else:
        while not(op == "S" or op == "N" or op == "s" or op == "n"):
            op = saveBand()
            if op == "n" or op == "N":
                return False
            elif op == 'S' or op == 's':
                return True
class NFSTools:
    def __init__(self):
        self._relaciones = list()
        self._carpetas = list()
        self._clientes = list()
        self._dns = list()
        self._clientes = list()
        self._ip = ""
        self._netmask = ""
        self._gateway = ""
        self._interface = ""
    def instalacion_paquetes_ubuntu(self):
        if self.isLinuxPlatform():
            system("clear")
            print(GREEN+"Instalación paquetes ubuntu")
            system('apt-get update')
            system('apt-get install nfs-kernel-server')
            print(GREEN+'Instalacion terminada...'+WHITE)
            time.sleep(2)   
        self.limpiarPantalla()    
    def config_ip(self):
        self.limpiarPantalla()
        if self.isLinuxPlatform() == True:
            self.setProperties()
            self.createIPFile()
            system('netplan try')
            system('netplan apply')
            system('systemctl restart networking')
            print("Configuracion realizada con exito....")
            self.limpiarPantalla()
    def createIPFile(self):
        try:
            path = ls('/etc/netplan')
            print(path)
            with open('01-network-manager-all.yaml','w') as ip:
                file_content = "network:\n version: 2\n ethernets:\n   {0}:\n     dhcp4: no\n     dhcp6: no\n     addresses: [{1}/{2}]\n     gateway4: {3}\n     nameservers:\n       "                                            .format(self._interface,self._ip,self._netmask,self._gateway)
                #Creamos el formato adecuado para colocar los servidores DNS y validamos que sean correctos
                dns_conf = "addresses: ["
                for x in self._dns:
                    dns_conf = dns_conf + x +","
                #Cerramos el corchete de la lista
                dns_conf = dns_conf[0:-1] +']'
                file_content = file_content + dns_conf
                ip.write(file_content)
                ip.close()
            print('mv 01-network-manager-all.yaml '+ path[0])
            system('mv 01-network-manager-all.yaml /etc/netplan/01-network-manager-all.yaml')
            print("Archivo creado exitosamente!!!")
            time.sleep(3)
        except FileExistsError:
            print("Error al abrir archivo")
        except FileNotFoundError:
            print("Error al crear archivo")
    def setIP(self):
        #Configuramos la IP de nuestro servidor
        self._ip = input("IP: ")
    def setNetmask(self):
        #Guardamos la mascara de red
        self._netmask = input("Mascara de red (numero de bits p.e 24 = 255.255.255.0): ")
    def setGw(self): #Guardamos el Gateway
        self._gateway = input("Digite la ip del gateway: ")
    def setDNS(self):
        #Funcion para guardar los DNS
        band = True
        while band == True:
            ip_dns = str(input("Digite la ip del servidor DNS: "))
            if not(ip_dns in self._dns):
                self._dns.append(ip_dns)
            band = validar("Desea gregar otro DNS (S/N): ")
    def setInterface(self):
        #Funcion para seleccionar una interfaz de red
        band = True
        print("Seleccione la interfaz de red: ")
        interfaces = netifaces.interfaces()
        def printInterfaces():
            for x in range(0,len(interfaces)):
                print(str(x)+ " " + interfaces[x])
        printInterfaces()
        select = int(input("N° Interfaz: "))
        while band:
                #Intentamos acceder al elemento de la lista que es de la tarjeta de red
            try:
                self._interface = str(interfaces[select])
                band = False
            except IndexError:
                #Obliga a seleccionar una interfaz valida
                band = True
                printInterfaces()
                select = int(input("N° Interfaz: "))
    def setProperties(self):
        self.setIP()
        self.setNetmask()
        self.setGw()
        self.setDNS()
        self.setInterface()
    def __str__(self):
        return self._ip + self._netmask + "\n" + self._gateway + "\n" + self._interface + '\n' + str(self._dns)
    def crear_carpeta(self):
        self.limpiarPantalla() 
        bandera = True
        while bandera:
            nombre = str(input("Nombre de la carpeta: "))
            if not(nombre in self._carpetas):
                self.exec('mkdir -p /var/nfs/{0}'.format(nombre))
                self.exec('chown nobody:nogroup /var/nfs/{0}'.format(nombre))
                self.exec('chmod 777 -R /var/nfs/{0}'.format(nombre))
                self._carpetas.append('/var/nfs/' + nombre)
                print(self._carpetas)
            bandera = validar("Desea agregar una carpeta (S/N)")
            self.limpiarPantalla()     
    def agregarClientes(self):
        self.limpiarPantalla()
        bandera = True
        while bandera:
            ip_cliente = str(input('Digite la ip del cliente: '))
            if not(ip_cliente in self._clientes):
                self._clientes.append(ip_cliente)
                print(self._clientes)
            else:
                print("El cliente ya se encuentra agregado a la lista")
            bandera = validar("Desea agregar otro cliente (S/N): ")
    def archivo_exports_clientes(self):
        def impresion():
            print("Clientes                 Carpetas")
            a = 0
            print(self._clientes)
            print(self._carpetas)
            for x in self._clientes:
                print("{0}.- {1}".format(a,x))
                a = a + 1
            a = 0
            for x in self._carpetas:
                print("{0}.- {1}".format(a,x))
                a = a + 1
            a = 0
        self.crear_carpeta()        
        self.agregarClientes()
        bandera = True     

        while bandera:
            self.limpiarPantalla()
            impresion()
            #Se puede mejorar la validacion
            x = int(input("Digite el numero de carpeta: "))
            y = int(input("Digite el numero de la ip mostrado el el menu por seleccionar: "))
            relacion = list()
            relacion.append(self._clientes[x])
            relacion.append(self._carpetas[y])
            relacion.append("rw")
            if not(relacion in self._relaciones):
                self._relaciones.append(relacion)
            bandera = validar("Desea agregar un cliente a una carpeta (S/N): ")
        
        with open("/etc/exports","w") as f:
            for x in self._relaciones:
                f.write("{1} {0}({2})\n".format(x[0],x[1],x[2]))
                f.close()
        self.limpiarPantalla()
    def configurarFirewall(self):
        self.limpiarPantalla()
        print(GREEN+"ACTIVANDO FIREWALL")
        system("ufw enable")
        system("ufw status")
        system("ufw allow 2049")
        print("LISTO.....")
        time.sleep(2)
        self.limpiarPantalla()
        pass
    def activarServidor(self):
        self.limpiarPantalla()
        system(GREEN+"systemctl restart nfs-kernel-server")
        print("Servicio activado")
        time.sleep(2)
        self.limpiarPantalla()
        pass
    def configurarCliente(self):

        self.limpiarPantalla()
        pass
    def isLinuxPlatform(self):
        name = sys()
        return name == 'Linux'
    def limpiarPantalla(self):
        if self.isLinuxPlatform() == False:
            self.exec('cls')
        else:
            self.exec('clear')
        pass
    def exec(self,strn, color = WHITE):
        print(strn)
        print(color+"", end = "")
        system(strn)
        time.sleep(0.3)
    def saveConfig(self):
        with open("conf.pickle", "wb") as f:
            pickle.dump(self, f)
    def loadConfig(self,str="conf.pickle"):
        try:
            with open(str, "rb") as inp:
                obj = pickle.load(inp)
                return obj
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass
        pass

    def imprimirMenu(self):
        print(YELLOW+"""    
       _   _______________________  ____  __   _____
      / | / / ____/ ___/_  __/ __ \\/ __ \\/ /  / ___/
     /  |/ / /_   \\__ \\ / / / / / / / / / /   \\__ \\ 
    / /|  / __/  ___/ // / / /_/ / /_/ / /______/ /  
   /_/ |_/_/    /____//_/  \\____/\\____/_____/____/
   
   [1]   -->INSTALAR PAQUETES DEL SERVIDOR NFS EN UBUNTU
   [2]   -->CONFIGURAR IP ESTATICA EN UBUNTU
   [3]   -->CREAR CARPETA
   [4]   -->CONFIGURAR ARCHIVO EXPORTS Y CLIENTES
   [5]   -->CONFIGURAR FIREWALL
   [6]   -->ACTIVAR SERVIDOR
   [7]   -->CONFIGURAR UN CLIENTE
   [8]   -->SALIR   
        """+WHITE)
        pass
    def menu(self):
        rep = True
        while rep == True:
            try:
                self.imprimirMenu()
                op = int(input(WHITE+"----->"))
                if op == 1:
                    self.instalacion_paquetes_ubuntu()
                elif op == 2:
                    self.config_ip()
                elif op == 3:
                    self.crear_carpeta()
                elif op == 4:
                    self.archivo_exports_clientes()
                elif op == 5:
                    self.configurarFirewall()
                elif op == 6:
                    self.activarServidor()
                elif op == 7:
                    self.configurarCliente()
                elif op == 8:
                    rep = False
                else:
                    raise ValueError
            except ValueError:
                self.limpiarPantalla()
                print(RED+"Digite una opción valida ........"+WHITE)
                rep = False
                time.sleep(1)
                self.menu()
        self.limpiarPantalla()
m = NFSTools()
if validar("Desea cargar las configuraciones (S/N): "):
    m = m.loadConfig()
m.menu()
m.saveConfig()