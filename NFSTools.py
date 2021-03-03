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
def inList(x, l = list()):
    for n in l:
        if n == x:
            return True
    l.append(x)
    return False
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
            self.limpiarPantalla()
            self.cambiarIP()
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

        string = "Direccion IP: " + self._ip + "/" +self._netmask + "\n"
        string = string + "Gateway: " + self._gateway + "\n"
        string = string + "Interfaz configurada: " + self._interface + '\n'
        string = string + "Servidores DNS: \n"
        for x in self._dns:
            string = string + "\t" + str(x) + "\n"
        string = string + "IP de clientes agregados:\n"
        for x in self._clientes:
            string = string + "\t" + str(x) + "\n"
        string = string + "Carpetas agregadas:\n"
        for x in self._carpetas:
            string = string + "\t" + str(x) + "\n"
        string = string + "Carpetas agregadas:\n"
        for x in self._relaciones:
            string = string + "\trelacion: {0} {1}({2})".format(x[0],x[1],x[2]) + '\n'   
        return string
    def crear_carpeta(self):
        self.limpiarPantalla() 
        bandera = True
        aux = self._carpetas
        while bandera:
            nombre = str(input("Nombre de la carpeta: "))
            if not(inList('/var/nfs/{0}'.format(nombre), aux)):
                self.exec('mkdir -p /var/nfs/{0}'.format(nombre))
                self.exec('chown nobody:nogroup /var/nfs/{0}'.format(nombre))
                self.exec('chmod 777 -R /var/nfs/{0}'.format(nombre))
                print(GREEN+'+++++Carpeta agregada'+WHITE)
            else:
                print(RED+'-----Carpeta en existencia'+WHITE)
            bandera = validar("Desea agregar una carpeta (S/N)")
            self.limpiarPantalla()     
        self._carpetas = aux
    def agregarClientes(self):
        self.limpiarPantalla()
        bandera = True
        aux = self._clientes
        while bandera:
            ip_cliente = str(input('Digite la ip del cliente: '))
            if not(inList(ip_cliente, aux)):
                print(GREEN+"+++++Cliente agregado"+WHITE)
            else:
                print(RED+"-----El cliente ya se encuentra agregado a la lista"+WHITE)
            bandera = validar("Desea agregar otro cliente (S/N): ")
        self._clientes = aux
    def archivo_exports_clientes(self):
        def impresion():
            if len(self._clientes) > 0 and len(self._carpetas) > 0:
                print("N    Clientes disponibles")
                a = 1
                for x in self._clientes:
                    print("{0}.- {1}".format(a,x))
                    a = a + 1
                a = 1
                print("N    Carpetas disponibles")
                for x in self._carpetas:
                    print("{0}.- {1}".format(a,x))
                    a = a + 1
            else:
                print(RED+"CLIENTES O CARPETAS NO DISPONIBLES")
        if validar("Desea agregar carpetas (S/N): "):
            self.crear_carpeta()
        if validar("Desea agregar clientes (S/N): "):      
            self.agregarClientes()
        if validar("Desea crear relaciones (S/N): "):
            if len(self._clientes) > 0 and len(self._carpetas) > 0:
                bandera = True     
                aux = self._relaciones
                while bandera:

                    self.limpiarPantalla()
                    impresion()
                    #Se puede mejorar la validacion
                    relacion = list()
                    band = True
                    while band:
                        try:
                            x = int(input("Digite el numero de carpeta: "))
                            relacion.append(self._carpetas[x-1])
                            band = False
                        except IndexError:
                            band = True

                    band = True

                    while band:
                        try:
                            y = int(input("Digite el numero de la ip del cliente, mostrado en el menu: "))
                            relacion.append(self._clientes[y-1])
                            band = False
                        except IndexError:
                            band = True

                    relacion.append("rw,sync,no_root_squash,no_subtree_check")

                    if not(inList(relacion, aux)):
                        print("Relacion agregada....")
                    else:
                        print("relacion existente....")

                    bandera = validar("Desea agregar un cliente a una carpeta (S/N): ")
                    self._relaciones = aux
        print("Creando archivo")
        time.sleep(3)
        with open('/etc/exports','w') as f:
            for t in self._relaciones:
                f.write("{0} {1}({2})".format(t[0],t[1],t[2]))
                f.write("\n")
            f.close()
        print("Archivo editado correctamente....")
        if validar("Desea activar el servicio NFS (S/N): "):
            self.activarServidor()
            print(YELLOW+"Estatus del servidor...")
            self.exec("systemctl status nfs-kernel-server")
            time.sleep(5)
        time.sleep(3)
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
        print(GREEN+"",end="")
        self.exec("systemctl restart nfs-kernel-server")
        self.exec("systemctl status nfs-kernel-server")
        print("Servicio activado")
        time.sleep(2)
        self.limpiarPantalla()
        pass
    def configurarCliente(self):
        self.limpiarPantalla()
        bandera = True
        self.exec("apt-get update")
        self.exec("apt-install nfs-common")
        while bandera:
            ip_servidor = str(input("Digite la ip del servidor: "))
            direccion_carpeta_servidor = str(input("Digite la ruta de la carpeta del servidor"))
            direccion_carpeta_cliente = str(input("Digite la ruta de la carpeta del cliente"))
            self.exec("mkdir -p " + direccion_carpeta_cliente)
            self.exec("mount {0}:{1} {2}".format(ip_servidor, direccion_carpeta_servidor, direccion_carpeta_cliente))
            bandera = validar("Desea montar otra carpeta (S/N): ")
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
    def cambiarIP(self):
        if len(self._ip) > 0 and len(self._netmask) > 0 and len(self._gateway) > 0 and len(self._interface) > 0 and len(self._dns) > 0:
            self.createIPFile()
            self.exec('netplan try')
            self.exec('netplan apply')
            self.exec('systemctl restart networking')
            print("Configuracion realizada con exito....")
        else:
            print("Falta configurar parametros...")
    def imprimirSubMenu(self):
        print(YELLOW+"""    
       _   _______________________  ____  __   _____
      / | / / ____/ ___/_  __/ __ \\/ __ \\/ /  / ___/
     /  |/ / /_   \\__ \\ / / / / / / / / / /   \\__ \\ 
    / /|  / __/  ___/ // / / /_/ / /_/ / /______/ /  
   /_/ |_/_/    /____//_/  \\____/\\____/_____/____/

                    <<<<cONFIGURACIONES ADICIONALES>>>>   
   [1]   -->CAMBIAR DIRECCION IP EN LA CONFIGURACION
   [2]   -->CAMBIAR SUBMASCARA DE RED EN LA CONFIGURACION
   [3]   -->CAMBAIAR GATEWAY  EN LA CONFIGRUACION
   [4]   -->CAMBIAR SERVIDORES DNS EN LA CONFIGURACION
   [5]   -->CAMBIAR INTERFAZ DE RED EN LA CONFIGURACION
   [6]   -->AGREGAR CLIENTES EN LA CONFIGURACION
   [7]   -->AGREGAR CARPETAS EN LA CONFIGURACION
   [8]   -->ELIMANR RELACION
   [9]   -->ELIMINAR CLIENTE
   [10]  -->ELIMINAR CARPETA
   [11]  -->Volver al Menu
        """+WHITE)
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
   [8]   -->CAMBIOS EN DATOS DEL SERVIDOR
   [9]   -->MOSTRAR INFO DE LAS CONFIGURACIONES
   [10]  -->SALIR   
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
                    self.submenu()
                    pass
                elif op == 9:
                    self.limpiarPantalla()
                    print(self)
                    input("Presione enter -------> ")
                    self.limpiarPantalla()
                    pass
                elif op == 10:
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
        m.saveConfig()
    def submenu(self):
        """ 
       _   _______________________  ____  __   _____
      / | / / ____/ ___/_  __/ __ \\/ __ \\/ /  / ___/
     /  |/ / /_   \\__ \\ / / / / / / / / / /   \\__ \\ 
    / /|  / __/  ___/ // / / /_/ / /_/ / /______/ /  
   /_/ |_/_/    /____//_/  \\____/\\____/_____/____/

                    <<<<cONFIGURACIONES ADICIONALES>>>>   
   [1]   -->CAMBIAR DIRECCION IP EN LA CONFIGURACION
   [2]   -->CAMBIAR SUBMASCARA DE RED EN LA CONFIGURACION
   [3]   -->CAMBAIAR GATEWAY  EN LA CONFIGRUACION
   [4]   -->CAMBIAR SERVIDORES DNS EN LA CONFIGURACION
   [5]   -->CAMBIAR INTERFAZ DE RED EN LA CONFIGURACION
   [6]   -->AGREGAR CLIENTES EN LA CONFIGURACION
   [7]   -->AGREGAR CARPETAS EN LA CONFIGURACION
   [8]   -->ELIMANR RELACION
   [9]   -->ELIMINAR CLIENTE
   [10]  -->ELIMINAR CARPETA
        """
        rep = True
        while rep == True:
            try:
                self.imprimirSubMenu()
                op = int(input(WHITE+"----->"))
                if op == 1:
                    self.setIP()
                elif op == 2:
                    self.setNetmask()
                elif op == 3:
                    self.setGw()
                elif op == 4:
                    self.setDNS()
                elif op == 5:
                    self.setInterface()
                elif op == 6:
                    self.agregarClientes()
                elif op == 7:
                    self.crear_carpeta()
                elif op == 8:
                    print("Aun sin funcionar")
                    pass
                elif op == 9:
                    print("Aun sin funcionar")
                    pass
                elif op == 10:
                    print("Aun sin funcionar")
                elif op == 11:
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
        print("En construccion....")
        time.sleep(4)
        pass
m = NFSTools()
if validar("Desea cargar las configuraciones (S/N): "):
    try:
        m = m.loadConfig()
    except:
        m = NFSTools()
m.limpiarPantalla()
m.menu()
