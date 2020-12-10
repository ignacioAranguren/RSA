#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:32:17 2020

@author: ignacio
"""
from sympy import randprime, isprime
from random import *
def rsa():
    mensaje = input('Introduzca el mesnaje a cifrar:')
    p = genPrimeP()
    q = genPrimeQ()
    n = p * q
    phi = (p-1)*(q-1)
    mensajeNum = sumMensaje(m)
    e = randint(1, phi)

    
# Algoritmo de Euclides Extendido
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

# inverso modular
def modInverse(a,m):
    L = egcd(a,m)
    return L[1] % m

# exponenciación modular y 
def mpow(x, y, z):
    e = 1
    while y:
        if y & 1:
            e = e * x % z
        y >>= 1
        x = x * x % z
    return e

#Suma todos los valores ascii de los caracteres del mensaje a base 10
def sumMensaje(m):
    L=list(map(ord, list(m)))
    l = len(L)
    L.reverse()
    M=0
    for i in range(l):
        M+=L[i]*(256**i)
    return M


def genPrimeP():
    primoAux = randprime(2**480,2**481)
    primo = 2 * primoAux + 1
    while isprime(primo)==False:
        primoAux = randprime(2**480,2**481)
        primo = 2*primoAux +1
    return primo
      
def genPrimeQ():
    primoAux = randprime(2**512, 2**513)
    primo = 2 * primoAux + 1
    while isprime(primo)==False:
        primoAux = randprime(2**512, 2**513)
        primo = 2*primoAux +1
    return primo