#!/usr/bin/env python3
import time
from os import system
from platform import system as sys
import netifaces
from os import listdir
from os.path import isfile, join
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

class NFSTools:
    def __init__(self):
        self._clientes = []
        self._ip = ""
        self._netmask = ""
        self._gateway = ""
        self._dns = []
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
            try:
                interfaces = netifaces.interfaces()
                band = True
                self._ip = input("Digite la dirección ip: ")
                self._netmask = input("Digite la mascara de red en formato /n [(p.e: /24)]: ")
                self._gateway = input("Digite la ip del gateway: ")
                while band == True:
                    def agregarOtroDNS():
                        op = input("Desea agregar otro servidor DNS (S/N): ")
                        return op
                    self._dns.append(input("Digite la ip del servidor DNS: "))
                    op = agregarOtroDNS()
                    if op == "S" or op == "N" or op == "s" or op == "n":
                        if op == "n" or op == "N":
                            band = False
                    else:
                        while not(op == "S" or op == "N" or op == "s" or op == "n"):
                            op = agregarOtroDNS()
                        if op == "n" or op == "N":
                            band = False
                band = True
                #Seleccionamos la interfaz
                print("Seleccione la interfaz de red: ")
                for x in range(0,len(interfaces)):
                    print(str(x)+ " " + interfaces[x])
                select = int(input("N° Interfaz: "))
                while band:
                    #Intentamos acceder al elemento de la lista que es de la tarjeta de red
                    try:
                        self._interface = str(interfaces[select])
                        band = False
                    except IndexError:
                        #Obliga a seleccionar una interfaz valida
                        band = True
                        select = int(input("N° Interfaz: "))
                #Se cierra el bucle y agrega la interfaz correcta
                #Abrimos creamos el archivo y lo editamos
                path = ls('/etc/netplan')
                print(path)
                with open('01-network-manager-all.yaml','w') as ip:
                    file_content = "network:\n  version 2\n  ethernets:\n    {0}:\n      dhcp4: no\n      dhcp6: no\n      addresses: [{1}/{2}]\n      gateway4: {3}\n      nameservers:\n        "                                            .format(self._interface,self._ip,self._netmask,self._gateway)
                    #Creamos el formato adecuado para colocar los servidores DNS y validamos que sean correctos
                    dns_conf = "addresses: ["
                    for x in self._dns:
                        dns_conf = dns_conf + x +","
                    #Cerramos el corchete de la lista
                    dns_conf = dns_conf[0:-1] +']'
                    file_content = file_content + dns_conf
                    ip.write(file_content)
                    ip.close()
                print('mv 01-network-manager-all.yaml '+path[0])
                system('mv 01-network-manager-all.yaml /etc/netplan/01-network-manager-all.yaml')
                print("Archivo creado exitosamente!!!")
                time.sleep(3)
            except FileExistsError:
                print("Error al abrir archivo")
            except FileNotFoundError:
                print("Error al crear archivo")
            system('netplan try')
            system('netplan apply')
            system('systemctl restart networking')
            print("Configuracion realizada con exito....")
            self.limpiarPantalla()
    def crear_carpeta(self):

        self.limpiarPantalla()
        pass
    def archivo_exports_clientes(self):
        
        self.limpiarPantalla()
        pass
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
    def exec(self,strn):
        system(strn)
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
                print(RED+"Digite una opción valida ........"+WHITE)
                rep = False
                time.sleep(1)
                self.menu()
        self.limpiarPantalla()
m = NFSTools()
m.menu()