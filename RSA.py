"""
Titulo: Metodo de cifrado RSA

Created on Fri Dec 11 14:39:36 2020

@author: Grupo 1

"""

from sympy import randprime, isprime
import os
from random import randint

def main():
    '''
    Metodo principal del programa0

    Returns
    -------
    None.

    '''
    cifrado=""
    flag = True
    while flag :
        print('')
        print('MENU DE CIFRADO RSA:')
        print('--------------------')
        print('1: Generar claves publica y privada')
        print('2: Cifrar')
        print('3: Descifrar')
        print('0: Salir')
        opc = input('Inserta opcion deseada: ')
        
        if opc == "1":
            _genClaves()
        
        if opc == "2":
           cifrado = _cifrar()
            
        if opc == "3":
            _descifrar(cifrado)
            
        if opc == "0":
            flag = False


def _genClaves():
    '''
    Metodo que genera claves aleartorias

    Returns
    -------
    None.

    '''
    p = _genPrimeP()
    q = _genPrimeQ()
    n = p * q
    phi = (p-1)*(q-1)
    e = _genE(p, q, phi)
    d = _modInverse(e, phi)
    
    print('Escribiendo claves en el archivo . . .')
    f=open("./clave.txt", "w")
    f.write(str(p)+"\n"+str(q)+"\n"+str(n)+"\n"+str(e)+"\n"+str(d))
    f.close()
    print("Claves escritas en el archivo clave.txt. . . ")
    
    print('Tu clave publica es: ')
    print('(', e, ', ', n, ')')
    print('')
    print('Tu clave privada es: ')
    print('(', d, ', ', n, ')')
    
    return [p,q,n,e,d]


def _egcd(a, b):
    '''
    Algoritmo extendido de Euclides

    Parameters
    ----------
    a : Int
        DESCRIPTION.
    b : Int
        DESCRIPTION.

    Returns
    -------
    list
        DESCRIPTION.

    '''
    x, X = 0, 1
    y, Y = 1, 0
    while (b != 0):
        B = b
        q = a // b
        a, b = b, a % b
        x, X = X - q * x, x
        y, Y = Y - q * y, y
    return ([B, X, Y])


def _genE(p,q, phi):
    '''
    Funcion para la generacion de e. Valor de la clave pública

    Parameters
    ----------
    p : Int
        Numero primo
    q : Int
        Numero primo
    phi : Int
        Resultado de realizar la operación (p-1)*(q-1)

    Returns
    -------
    e : Integer
        Valor e de la clave pública (e, n)

    '''
    e = randint(1,phi)
    gcd = _egcd(phi,e)
    divisor = gcd[0]
    
    while divisor != 1:
        e = randint(1,phi)
        gcd = _egcd(phi,e)
        divisor = gcd[0]
    
    return e


def _modInverse(a,m):
    '''
    Función que calcula el modulo inverso de dos valores

    Parameters
    ----------
    a : Int
        DESCRIPTION.
    m : Int
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    L = _egcd(a,m)
    return L[1] % m


def _genPrimeP():
    '''
    Funcion que genera un numero primo

    Returns
    -------
    primo : Int
        Numero primo

    '''
    primoAux = randprime(2**480,2**481)
    primo = 2 * primoAux + 1
    while isprime(primo)==False:
        primoAux = randprime(2**480,2**481)
        primo = 2*primoAux +1
    return primo
      

def _genPrimeQ():
    '''
    Funcion que genera un numero primo

    Returns
    -------
    primo : Int
        Numero primo    
    
    '''
    primoAux = randprime(2**512, 2**513)
    primo = 2 * primoAux + 1
    while isprime(primo)==False:
        primoAux = randprime(2**512, 2**513)
        primo = 2*primoAux +1
    return primo

def leerFichero():
    '''
    Función para lectura del fichero de claves

    Returns
    -------
    list
        DESCRIPTION.

    '''
    f = open("./clave.txt")
    p = int(f.readline())
    q = int(f.readline())
    n = int(f.readline())
    e = int(f.readline())
    d = int(f.readline())  
    f.close()
    return [p,q,n,e,d]


def _cifrar():
    '''
    Metodo que cifra un mensaje

    Returns
    -------
    cifrado.

    '''
    if(os.path.isfile("./clave.txt")==True and os.stat("./clave.txt").st_size != 0):
        print("\nLeyendo claves del fichero ./claves.txt ....")
        p,q,n,e,d = leerFichero()       
        print("Claves cargadas con éxito")
    else:
        res=''
        print("No hay claves claves creadas.")
        while res != 'N' and res != 'n' and res!= 's' and res != 'S':
            res = input('¿Quieres introducir manualmente las claves? (S/N)')
            if(res == 'N' or res == 'n'): 
                print("Generando claves")
                p,q,n,e,d= _genClaves()
            elif(res== 's' or res == 'S'):
                print('Inserta tu clave:\n') 
                e = int(input('e = '), 10)
                n = int(input('n = '), 10)
            else: print("Respuesta no válida")
    print('\n\nCifrar mensaje')
    print('-----------------')
    flag = True
    while flag:
        mensaje = input('Inserta el mensaje : ')
        if len(mensaje) >124:
            flag = True
            print('### ERROR ###')
            print('El mensaje tiene que ser como máximo de 124 bytes. ')
            print('Tamaño de mensaje ----> '+str(len(mensaje))+ "\n")
        else:
            flag = False
            mensajeNum = _base10(mensaje)
            cifrado = _mpow(mensajeNum, e, n)
            ##num= convertBase256(cifrado)
            print("\n Mensaje cifrado es: "+str(cifrado))

    return cifrado

def _descifrar(cifrado):
    '''
    Metodo que descifra un mensaje

    Returns
    -------
    None.

    '''
    print('')
    print('')
    print('Descifrar mensaje')
    print('-----------------')
    res = "n"
    if(os.path.isfile("./clave.txt")==True and os.stat("./clave.txt").st_size != 0):
            print("\nLeyendo claves del fichero ./claves.txt ....")
            p,q,n,e,d = leerFichero()       
            print("Claves cargadas con éxito")      
    else:
        res=''
        print("No hay claves claves creadas.")
        while res != 'N' and res != 'n' and res!= 's' and res != 'S':
            res = input('¿Quieres introducir manualmente las claves? (S/N)')
            if(res == 'N' or res == 'n'): 
                print("Generando claves")
                p,q,n,e,d  = _genClaves()
            elif(res== 's' or res == 'S'):
                print('Inserta tu clave:\n')
                d = int(input('e = '), 10)
                n = int(input('n = '), 10)
            else: print("Respuesta no válida")
    if(str(cifrado) != ""):
        res = input("Hay un mensaje ya cifrado, ¿quieres descifrar ese u otro? (S/N)")
        if(res == 'S' or res == 's'):
           print("\n Mensaje cifrado: "+str(cifrado)+"\n")
           mensaje = _mpow(int(cifrado), d, n)
           num = _convertBase256(mensaje)
           print("\nMensaje descifrado: ", _valorAscii(num))
    if(str(cifrado) == "" or (res != 's' and res != 'S')):
       try:
            cripto = input('Inserta el mensaje cifrado: ')
            mensaje = _mpow(int(cripto), d, n)
            num = _convertBase256(mensaje)
            print("\nMensaje descifrado: ", _valorAscii(num))
       except ValueError:
            print('El valor debe de ser numérico')

def _mpow(x, y, z):
    '''
    Función que calcula la exponenciacion modular

    Parameters
    ----------
    x : Int
        DESCRIPTION.
    y : Int
        DESCRIPTION.
    z : Int
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    e = 1
    while y:
        if y & 1:
            e = e * x % z
        y >>= 1
        x = x * x % z
    return e


def _base10(m):
    '''
    Función que suma todos los valores ascii de los caracteres del mensaje a base 10

    Parameters
    ----------
    m : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    L=list(map(ord, list(m)))
    l = len(L)
    L.reverse()
    M=0
    for i in range(l):
        M+=L[i]*(256**i)
    return M


def _convertBase256(n):
    '''
    Función que convierte a base 256 un mensaje.
    
    Recibe como entrada valores enteros en base 10 y lo convierte a una lista
    de caractares en base256.La función to_bytes() convierte el entero a bytes,
    metiendo en cada posición de la lita el valor decimal de 0 a 255 de cada byte
    en big enddian.

    Parameters
    ----------
    m : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return list(n.to_bytes((n.bit_length() +7 )//8, 'big'))


def _valorAscii(n):
    '''
    Funcion que convierte a ascii un mensaje cifrado

    Parameters
    ----------
    n : TYPE
        DESCRIPTION.

    Returns
    -------
    cadena : TYPE
        DESCRIPTION.

    '''
    cadena=''
    for i in range(len(n)):
        if(n[i]!=0): cadena+=chr(n[i])
    return cadena
        
if __name__ == "__main__":
    main()