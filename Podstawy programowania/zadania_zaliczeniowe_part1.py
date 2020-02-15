#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:08:02 2020

@author: MaciejMiernicki
"""
#Wylosowane zadania: [1, 2, 4, 8, 14, 17, 24, 25, 27, 28, 30, 31, 32]

import numpy as np
import matplotlib.pyplot as plt

#1. Napisz skrypt, który będzie wyświetlać wszystkie kolejne dzielniki wprowadzonej liczby

def dzielniki(x):
    temp1 = list()
    for i in range(1,int(x/2 + 1)):
        if x%i == 0:
            temp1.append(i)
    temp1.append(x)
    return temp1

#2. Korzystając z pojęcia funkcji utwórz skrypt, który będzie miał możliwość zamiany temperatury 
#pomiędzy skalami Celsjusza i Fahrenheita (w obie strony). C = (F-32)x(5/9), F = (C*9/5)+32
    
def konwTemp(x):
    print('''Podaj jak chcesz zamienić temperaturę
          1. Celciusz -> Fahrenheit
          2. Fahrenheit -> Celciusz''')
    t1 = int(input())
    t2 = 0
    if t1 == 1:
        t2 = (x*9/5)+32
    elif t1 == 2:
        t2 = (x-32)*(5/9)
    else: 
        print('Podałeś niepoprawną opcję')
    return t2

#4. Utwórz skrypt do znajdowania miejsc zerowych trójmianu kwadratowego 
# x1 = (-b+sqrt(b*b-4*a*c))/(2*a)
# x2 = (-b-sqrt(b*b-4*a*c))/(2*a)

def miejscaZerowe(a,b,c):
    delta = b**2-4*a*c
    if delta == 0:
        x1 = (-b)/(2*a)
        print('''Tylko jedno miejsce zerowe:
              x1 = ''',x1)
    elif delta>0:
        x1 = (-b+delta**-1)/(2*a)
        x2= (-b-delta**-1)/(2*a)
        print('''Miejsca zerowe twojej funkcji to:
              x1 = ''',x1,'''
              x2 = ''',x2)
    else: 
        print('Funkcja nie ma miejsc zerowych!')
            
        

#8. W klasie przeprowadzono sprawdzian, za który uczniowie mogli otrzymać maksymalnie 40 punktów. 
#Skala ocen w szkole jest następująca: 0-39% - ndst, 40-49% - dop, 50-69% - dst, 70-84% - db, 
# 85-99% - bdb, 100% - cel. Utwórz skrypt z interfejsem tekstowym, który na podstawie podanej 
#liczby punktów ze sprawdzianu wyświetli ocenę jaka się należy (skorzystaj z konstrukcji if, elif, else)

def liczOcene():
    a = float((input('''Podaj ile pkt. otrzymałeś na sprawdzanie:
    ''')))*2.5
        
    if a <= 39:
        print('Twoj ocena to ndst')
    elif a <= 49:
        print('Twoj ocena to dop')
    elif a<= 69:
        print('Twoja ocena to dst')
    elif a<= 84:
        print('Twoja ocena to db')
    elif a<= 99:
        print('Twoja ocena to bdb')
    else:
        print('Twoja ocena to cel')

#14. Utworzyć skrypt z interfejsem tekstowym, który będzie zwracać wiersz 
#n-tego rzędu z trójkąta Pascala (użytkownik podaje n, program zwraca odpowiadający wiersz trójkąta)

def trojkPasc():       
    print('Podaj który wiersz trójkąta Pascala chcesz poznać:')
    a = int(input())
    
    def trojkatPasc(a):
        x1 = np.ones(1)
        x2 = np.ones(2)
        if a == 1:
            return x1
        elif a == 2:
            return x2
        else:
            x1 = np.ones(3, dtype = int)
            for i in range(2,a):
                x2 = np.ones(i+1, dtype = int)
                for j in range(1,i):
                    x2[j] = x1[j-1] + x1[j]
                x1 = x2
            return x2
            
    print('Oto twój wiersz trójkąta Pascala:')
    wynik = trojkatPasc(a)
    print(','.join([str(x) for x in wynik]))

#17. Utwórz funkcję, która będzie generować listy danych do wykreślenia w oparciu o:
#a) fukcję liniową ax+b
#b) funkcję kwadratową ax^2+bx+c
#c) funkcję odwrotnie-potęgową a/x^n
#Każda z fukcji powinna przyjmować parametry równania, 
#natomiast zwracać powinna dwie listy - x i y, które następnie będzie można wykreślić na wykresie
def isPositive(x):
    if x>=0:
        return '+'
    else:
        return '-'
    
def listDanych():
    plt.cla()
    listaX = np.arange(-15,15)
    listaY = list()
    print('''Wybierz typ funkcji: 
         1 -  fukcja liniowa ax+b
         2 -  funkcja kwadratowa ax^2+bx+c
         3 - funkcja odwrotnie-potęgowa a/x^n ''')
    temp1 = int(input())
    if temp1 == 1:
        print('Podaj parametry a i b funkcji linowej ax+b')
        a = int(input('a:'))
        b = int(input('b:'))
        for i in range(-15,15):
            temp1 = a*i+b
            listaY.append(temp1)
        print('''lista wartości to:''',
              listaY,''' dla x od 0 do 100''')
        print('''Czy chcesz wykreślić funkcję na wykresie?
              Y - tak
              N - nie''')
        temp1 = str(input())
        if temp1 == 'Y' or temp1 == 'y':
            plt.plot(listaX, listaY)
            plt.plot((-15,15),(0,0), linestyle = '--', linewidth = 0.9, color = 'k')
            plt.plot((0,0),(min(listaY),max(listaY)), linewidth = 0.9, linestyle = '--', color = 'k')
            plt.xlabel('x')
            plt.ylabel("{a}x{b1}{b}".format(a=a, b1=isPositive(b) ,b=abs(b)))
    elif temp1 == 2:
        print('Podaj parametry a, b i c funkcji kwadratowej ax^2+bx+c')
        a = int(input('a:'))
        b = int(input('b:'))
        c = int(input('c:'))
        for i in range(-15,15):
            temp1 = a*i**2+b*i+c
            listaY.append(temp1)
        print('''lista wartości to:''',
              listaY,''' dla x od 0 do 100''')
        print('''Czy chcesz wykreślić funkcję na wykresie?
              Y - tak
              N - nie''')
        temp1 = str(input())
        if temp1 == 'Y' or temp1 == 'y':
            plt.plot(listaX, listaY)
            plt.plot((-15,15),(0,0), linestyle = '--', linewidth = 0.9, color = 'k')
            plt.plot((0,0),(min(listaY),max(listaY)), linewidth = 0.9, linestyle = '--', color = 'k')
            plt.xlabel('x')
            plt.ylabel("{a}x^2{b1}{b}x{c1}c".format(a=a, b1=isPositive(b), b=abs(b), c1=isPositive(c), c=abs(c)))
    elif temp1 == 3:
        print('Podaj parametry a i n funkcji odwrotnie potęgowej a/x^n')
        a = int(input('a:'))
        n = int(input('n:'))
        for i in range(-15,15):
            if i == 0 and n>0:
                listaY.append(None)
            elif i == 0 and n<0:
                listaY.append(0)
            else:
                temp1 = a/i**n
                listaY.append(temp1)                
        print('''lista wartości to:''',
              listaY,''' dla x od 0 do 100''')
        print('''Czy chcesz wykreślić funkcję na wykresie?
              Y - tak
              N - nie''')
        temp1 = str(input())
        if temp1 == 'Y' or temp1 == 'y':
            plt.plot(listaX, listaY)
            listaY[15] = 0
            plt.plot((-15,15),(0,0), linestyle = '--', linewidth = 0.9, color = 'k')
            plt.plot((0,0),(min(listaY),max(listaY)), linewidth = 0.9, linestyle = '--', color = 'k')
            plt.xlabel('x')
            plt.ylabel("{a}/x^{n}".format(a=a, n=n))
    else:
        print('Podałeś niepoprawny wybór')

        

