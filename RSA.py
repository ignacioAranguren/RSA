#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:32:17 2020

@author: ignacio
"""
from sympy import randprime, isprime
from random import *
from os import system

################################################
#    Algoritmo de Euclides Extendido
################################################

def egcd(a, b):
    x, X = 0, 1
    y, Y = 1, 0
    while (b != 0):
        B = b
        q = a // b
        a, b = b, a % b
        x, X = X - q * x, x
        y, Y = Y - q * y, y
    return ([B, X, Y])

################################################
#    Obtención número e
################################################

def genE(p,q, phi):
    e = randint(1,phi)
    gcd = egcd(phi,e)
    divisor = gcd[0]
    while divisor != 1:
        e = randint(1,phi)
        gcd = egcd(phi,e)
        divisor = gcd[0]
    return e

################################################
#   Inverso modular
################################################
def modInverse(a,m):
    L = egcd(a,m)
    return L[1] % m

################################################
#   Generación de número primo p seguro
################################################

def genPrimeP():
    primoAux = randprime(2**480,2**481)
    primo = 2 * primoAux + 1
    while isprime(primo)==False:
        primoAux = randprime(2**480,2**481)
        primo = 2*primoAux +1
    return primo
      
################################################
#   Generación de número primo q seguro
################################################

def genPrimeQ():
    primoAux = randprime(2**512, 2**513)
    primo = 2 * primoAux + 1
    while isprime(primo)==False:
        primoAux = randprime(2**512, 2**513)
        primo = 2*primoAux +1
    return primo


######### Declariación variables globales #########
p = genPrimeP()
q = genPrimeQ()
n = p * q
phi = (p-1)*(q-1)
e = genE(p, q, phi)
d = modInverse(e, phi)


################################################
#    Cifrado RSA
################################################
def rsa():
    try:
        mensaje = input('Introduzca el mensaje a cifrar: ')
        if(len(mensaje)>124): raise NameError('MaxMessageSizeException')
        mensajeNum = base10(mensaje)
        cifrado = mpow(mensajeNum, e, n)
        num= convertBase256(cifrado)
        print("\nMensaje cifrado con formato ASCII: "+valorAscii(num))
        print("\n Mensaje cifrado numérico: "+str(cifrado))
    except NameError:
        print('\n###########################################################')
        print('El mensaje tiene que ser como máximo de 124 bytes. ')
        print('Tamaño de mensaje ----> '+str(len(mensaje))+ "\n")
    return cifrado

################################################
#    Desifrado RSA
################################################
def descifrado(cripto):
    #cripto = base10(cripto)
    mensaje = mpow(int(cripto), d, n)
    num = convertBase256(mensaje)
    print ("\nMensaje descifrado: " + valorAscii(num))
    
    
################################################
#    Exponenciación modular
################################################
# exponenciación modular y 
def mpow(x, y, z):
    e = 1
    while y:
        if y & 1:
            e = e * x % z
        y >>= 1
        x = x * x % z
    return e

################################################
#    Conversión de mensaje a valores númericos
################################################
#Suma todos los valores ascii de los caracteres del mensaje a base 10

def base10(m):
    L=list(map(ord, list(m)))
    l = len(L)
    L.reverse()
    M=0
    for i in range(l):
        M+=L[i]*(256**i)
    return M

################################################
#    Conversión de mensaje en base 256
################################################

"""
Recibe como entrada valores enteros en base 10 y lo convierte a una lista
 de caractares en base256.La función to_bytes() convierte el entero a bytes,
 metiendo en cada posición de la lita el valor decimal de 0 a 255 de cada byte
 en big enddian.
"""

def convertBase256(n):
    return list(n.to_bytes((n.bit_length() +7 )//8, 'big'))


################################################
#    Conversión de mensaje a valor ascii
################################################
#Convierte la lista de vlaores en bas e256 a su correspodiente valo ASCII
def valorAscii(n):
    cadena=''
    for i in range(len(n)):
        if(n[i]!=0): cadena+=chr(n[i])
    return cadena
        
def main():
    op = 0 
    cif = ''
    while op==0:
        print("\n1- Cifrar")
        print("2- Descifrar")
        print("0- Salir")
        op = input("\n Selecciona una opción: ")
        if(int(op) == 1): 
            cif = rsa()
            op=0
        elif(int(op)==2):
            if(cif == ''):
                cripto = input("Criptograma (valor númerico): ")
            else: 
                res = input('¿Quieres cifrar el mensaje que has cifrado antes? (S/N)')
                if(res == 'S' or res == 's'): cripto = cif
                else: cripto = input("Criptograma (valor númerico): ")
            descifrado(cripto)
            op = 0
        elif(int(op)==0):
            op=1
            print('Adiós')
        else: print("Opción inválida.")
        
if __name__ == "__main__":
    main()