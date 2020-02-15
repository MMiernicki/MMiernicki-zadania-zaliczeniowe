#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:08:02 2020

@author: MaciejMiernicki
"""
#Wylosowane zadania: [1, 2, 4, 8, 14, 17, 24, 25, 27, 28, 30, 31, 32]
import numpy as np
import matplotlib.pyplot as plt
import collections as cl

#24. Utwórz fukcję, która jako argument będzie przyjmować listę liczb zmiennoprzecinkowych, 
# a jej wynikiem będzie odchylenie standardowe średniej

def stdDev(x):
    xMean = np.mean(x)
    stdSuma = 0
    for i in range(len(x)):
        stdSuma = stdSuma + (x[i] - xMean)**2
    stdSuma = stdSuma/len(x)
    return np.sqrt(stdSuma)

#25. Utwórz fukcję, która jako argument będzie przyjmować listę liczb zmiennoprzecinkowych, 
# a jej wynikiem będzie drugi moment centralny (wariancja)
    
def calcWari(x):
    return stdDev(x)**2

#27. Utwórz funkcję, która jako argument będzie przyjmować listę liczb zmiennoprzecinkowych, 
# a jej wynikiem będzie czwarty moment centralny (kurtoza)

def calcKurt(x):
    suma = 0
    sr = np.mean(x)
    for i in range(len(x)):
        suma = suma + (x[i] - sr)**4
    return (((1/stdDev(x)**4)*(suma/len(x)))-3)

#28. Utwórz funkcję, która jako argument będzie przyjmować dwie listy o równej liczbie elementów, 
# a jej wynikiem będzie współczynnik korelacji

def calcKorel(x,y):
    if len(x) != len(y):
        return('Listy muszą mieć taką samą długość')
    else:
        sumaXY = 0
        sumaX = 0
        sumaY = 0
        sumaX2 = 0
        sumaY2 = 0
        
        for i in range(len(x)):
            sumaXY += x[i]*y[i]
            sumaX += x[i]
            sumaY += y[i]
            sumaX2 += x[i]**2
            sumaY2 += y[i]**2
            
        c1 = (len(x) * sumaXY - sumaX*sumaY)
        c2 = np.sqrt((len(x) * sumaX2 - sumaX**2)*(len(y) * sumaY2 - sumaY**2))
        
        return c1/c2

#30. Wynegeruj listę 1000 liczb losowych o rozkładzie normalnym. 
# Wykreśl histogram oraz średnią, medianę, dominantę, odchylenie standardowe, wariancję, skośność i kurtozę
        
def calcDomin(x):
    return cl.Counter(x).most_common()[0][0]

def calcSkos(x):
    suma = 0
    sr = np.mean(x)
    for i in range(len(x)):
        suma = suma + (x[i] - sr)**3
    return ((suma/len(x))*(1/stdDev(x)**3))    
    
def randomStats():
   a = np.random.standard_normal(size = 1000)
   plt.cla()
   plt.hist(a, bins = 25, facecolor='g', alpha = 0.75)
   a1 = np.histogram(a, bins = 25)
   z = np.max(a1[0])
   plt.ylabel('Ilość')
   plt.xlabel('Wartość')
   plt.plot((np.mean(a),np.mean(a)),(0,z),label = 'Średnia = {z}'.format(z = round(np.mean(a), ndigits = 2)), color = 'b')
   plt.plot((np.median(a),np.median(a)),(0,z),label = 'Mediana = {z}'.format(z = round(np.median(a), ndigits = 2)), color = 'r')
   plt.plot((calcDomin(a),calcDomin(a)),(0,z),label = 'Dominanta = {z}'.format(z = round(calcDomin(a), ndigits = 2)), color = 'c')
   plt.plot((stdDev(a),stdDev(a)),(0,z),label = 'Odchylenie std. = {z}'.format(z = round(stdDev(a), ndigits = 2)), color = 'm')
   plt.plot((calcWari(a),calcWari(a)),(0,z),label = 'Wariancja = {z}'.format(z = round(calcWari(a), ndigits = 2)), color = 'y')
   plt.plot((calcSkos(a),calcSkos(a)),(0,z),label = 'Skośność = {z}'.format(z = round(calcSkos(a), ndigits = 2)), color = 'k')
   plt.plot((calcKurt(a),calcKurt(a)),(0,z),label = 'Kurtoza = {z}'.format(z = round(calcKurt(a), ndigits = 2)), color = 'blueviolet')
   plt.legend()
   
#31. Korzystając z instrukcji np.random.choice oraz reshape z pakietu numpy stworzyć funkcję 
# generują macierz kwadratową stopnia N wypełnioną wartościami 0 i 255 w losowy sposób
   
def arrayOfN(n):
    z = np.arange(0,256)
    z1 = np.random.choice(z, size=n**2)
    z1 = np.reshape(z1, (n,n))
    return z1

#32. Utwórz funckję, która na zadanej macierzy zapisze wzór ustalonych struktur 
# (blok, ul, bochenek, łódka, światła uliczne, żaba, latarnia)
    
def dodajElement(grid):
    temp1 = None
    while temp1 !=0:
        print('''Wybierz jaki element chcesz dodać do macierzy:
              1. Blok
              2. Ul
              3. Bochenek
              4. Łódka
              5. Światła uliczne
              6. Żaba
              7. Latarnia
              0. Koniec programu''')
        temp1 = int(input())
        tab = grid
        blok = ([0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0])
        ul = ([0,0,0,0,0,0],[0,0,1,1,0,0], [0,1,0,0,1,0], 
              [0,0,1,1,0,0], [0,0,0,0,0,0])
        bochenek = ([0,0,0,0,0,0],[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,1,0,1,0],
                    [0,0,0,1,0,0],[0,0,0,0,0,0])
        lodka = ([0,0,0,0,0],[0,1,1,0,0],[0,1,0,1,0],[0,0,1,0,0],[0,0,0,0,0])
        swiatla = ([0,0,0,0,0,0],[0,1,1,0,0,0],[0,1,1,0,0,0],
                   [0,0,0,1,1,0],[0,0,0,1,1,0],[0,0,0,0,0,0])
        zaba = ([0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,1,1,0],
                   [0,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0])
        latarnia = ([0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],
                   [0,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0])
        elementy = ([blok, ul, bochenek, lodka, swiatla, zaba, latarnia])
        l1 = len(tab)
        l2 = len(tab[0])
        if temp1 != 0:
            if l1<len(elementy[temp1-1]) or l2<len(elementy[temp1-1][0]):
                print('Macierz jest za mała aby pomieścić ten obiekt!')
            else:
                i = np.random.randint(0,l1-len(elementy[temp1-1]))
                print(i)
                j = np.random.randint(0,l2-len(elementy[temp1-1][0]))
                print(j)
                tab[i:i+len(elementy[temp1-1]), j:j+len(elementy[temp1-1][0])] = elementy[temp1-1]
    return tab