#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 09:24:07 2020

@author: MaciejMiernicki
"""
import json
import datetime as dt
import os
import sys

class SlowoDoNauki:
    
    def __init__(self, slowo: str, tlumaczenie: str, caseSensitive: bool = False, nextAnswerDate: dt.date = dt.date.today()):
        self.slw = slowo
        self.tlm = tlumaczenie
        self.caseSensit = False
        self.nextAnswDate = dt.date.today()
        
    def __repr__(self) -> str:
        return str(' <-> '.join([self.slw, self.tlm]))
        
    def pytaj(self) -> bool:
        if self.caseSensit == False:
            odp = str(input('{x}: '.format(x = self.slw)))
            if odp.lower() == self.tlm.lower():
                print('Dobra odpowiedź!')
                self.nextAnswDate = self.nextAnswDate + dt.timedelta(days=7) 
            else:
                print('Zła odpowiedź, spróbuj następnym razem!')  
        else:
            odp = str(input('{x}: '.format(x = self.slw)))
            if odp == self.tlm:
                print('Dobra odpowiedź!')
            else:
                print('Zła odpowiedź, spróbuj następnym razem!')
                self.nextAnswDate = self.nextAnswDate + dt.timedelta(days=7)   
                
    def modyfikuj(self, slowo: str, tlumaczenie: str, caseSensitive: str) -> None:
        self.slw = slowo
        self.tlm = tlumaczenie
        if caseSensitive.lower() == 'y':
            self.caseSensit = True
        else:
            self.caseSensit = False
            
def nowa_lista() -> list:
    z = int(input('Podaj ilość słów: '))
    slowa = list([z])
    
    for i in range(slowa[0]):
        inp1 = str(input('Podaj {x} słowo: '.format(x = i+1)))
        inp2 = str(input('Podaj tłumaczenie: '))
        temp = SlowoDoNauki(inp1,inp2)
        slowa.append(temp)
    return slowa

def odpytuj(listaSlow:list) -> None:
    
    try:
        
        for i in range(1,listaSlow[0]+1):
            if listaSlow[i].nextAnswDate == dt.date.today() or listaSlow[i].nextAnswDate < dt.date.today():
                listaSlow[i].pytaj()
        print('Koniec nauki. Data następnej sesji: {z}'.format(z = str(dt.date.today() + dt.timedelta(days=7))))
        print('Rozpoczynam zapisywanie listy.')
        zapisz_liste(listaSlow)
        print('Plik został zapisany. Wyłączam program.')
    except:
        print('Zły typ pliku z słówkami. Zamykam program.')
        sys.exit('')

           
def list_to_dict(listaSlow:list) -> dict:
    a = dict()
    a['0'] = listaSlow[0]
    
    for i in range(1,listaSlow[0]+1):
        
        try:
            z = str(i)
            a[z] = dict()
            a[z]['Słowo'] = listaSlow[i].slw
            a[z]['Tłumaczenie'] = listaSlow[i].tlm
            a[z]['Case Sensitive'] = listaSlow[i].caseSensit
            a[z]['Data przyszłej nauki D'] = listaSlow[i].nextAnswDate.day
            a[z]['Data przyszłej nauki M'] = listaSlow[i].nextAnswDate.month
            a[z]['Data przyszłej nauki Y'] = listaSlow[i].nextAnswDate.year
        except:
            print('Zły typ pliku z słówkami. Zamykam program.')
            sys.exit('')
            
    return a

def zapisz_liste(slowa:list) -> None:
    listaSlow = list_to_dict(slowa)
    json_temp = json.dumps(listaSlow)
    nazwa = str(input('Podaj jaką nazwę chcesz nadać swojej liście słów: '))
    path = os.getcwd()
    odp = str(input('Czy zapisać plik w lokalizacji {z}? Tak - Y, Nie - N: '.format(z = path))).lower()
    
    if odp == 'y':
        f = open(''.join([nazwa,'.json']),'w')
        f.write(json_temp)
        f.close()
        
    elif odp == 'n':
        gdzieZapisac = str(input('Podaj ścieżkę gdzie mam zapisać listę słów:'))
        
        try:
           os.chdir(gdzieZapisac)
           f = open(''.join([nazwa,'.json']),'w')
           f.write(json_temp)
           f.close()
        except:
            print('Podałeś złą ścieżkę do zapisu pliku. Plik został zapisany w lokalizacji {z}'.format(os.getcwd()))
            f = open(''.join([nazwa,'.json']),'w')
            f.write(json_temp)
            f.close()
    else:
        print('Wprowadź poprawną odpowiedź')

def wczytaj_liste() -> list:
    path = os.getcwd()
    print('Czy plik znajduje się w ścieżce: {z}? Tak - Y, Nie - N'.format(z = path))
    odp = str(input()).lower()
    listaSlowDict = dict()
    
    if odp == 'y':
        print('Podaj nazwę pliku (bez rozszerzenia): ')
        nazwaPliku = str(input())
        
        try:
            f = open(''.join([nazwaPliku,'.json']), 'r')
            listaSlowDict = json.loads(f.read())
            f.close()
            return dict_to_list(listaSlowDict)
        except:
            print('W podanej ścieżce nie ma takiego pliku. Zamykam program.')
            sys.exit('')
        
    elif odp == 'n':
        gdzieZapisac = str(input('Podaj ścieżkę gdzie znajduje się plik z listą słów:'))
        try:
           os.chdir(gdzieZapisac)
        except:
            print('Podałeś złą ścieżkę do wczytania pliku. Zamykam program.')
            sys.exit('')
        print('Podaj nazwę pliku(bez rozszerzenia): ')
        nazwaPliku = str(input())
        try:
            f = open(''.join([nazwaPliku,'.json']), 'r')
            listaSlowDict = json.loads(f.read())
            f.close()
            return dict_to_list(listaSlowDict)
        except:
            print('W podanej ścieżce nie ma takiego pliku. Zamykam program.')
            sys.exit('')
            
    else:
        print('Wprowadziłeś niepoprawną odpowiedź, zamykam program.')

def dict_to_list(jsonDump:dict) -> list:
    listaSlowList = list()
    listaSlowList.append(int(jsonDump['0']))
    
    for i in range(1,int(jsonDump['0'])+1):
        tempList = list()
        z = str(i)
        tempList.append(jsonDump[z]['Słowo'])
        tempList.append(jsonDump[z]['Tłumaczenie'])
        tempList.append(jsonDump[z]['Case Sensitive'])
        tempList.append(jsonDump[z]['Data przyszłej nauki Y'])
        tempList.append(jsonDump[z]['Data przyszłej nauki M'])
        tempList.append(jsonDump[z]['Data przyszłej nauki D'])
        answerDate = dt.date(tempList[3],tempList[4],tempList[5])
        tempSlowo = SlowoDoNauki(tempList[0],tempList[1],tempList[2],answerDate)
        listaSlowList.append(tempSlowo)
        
    return listaSlowList

def dodaj_słówka(plikSlowa:list) -> list:
    
    tempLista = plikSlowa
    print('Rozpoczynamy proces dodawania słówek do istniejącego pliku')
    noweSlowa = nowa_lista()
    
    try:
        tempLista[0] = tempLista[0] + noweSlowa[0]
        for i in range(1,len(noweSlowa)):
            tempLista.append(noweSlowa[i])
        print('Słowa dodane - przechodzimy do zapisywania.')
        zapisz_liste(tempLista)
        return tempLista
    except:
        print('Coś poszło nie tak - może wczytałeś zły plik. Zamykam program.')
        sys.exit('')
        
def modyfikuj(plikSlowa:list) -> list:
    print('Witaj w edytorze pliku słówek. Oto lista słówek w twoim pliku:')
    for i in range(1,len(plikSlowa)):
        
        print('Para słów {x}: {y}, {z}, Case Sensitive: {u}, Data następnej odpowiedzi: {w}'.format(x = i, y = plikSlowa[i].slw, z = plikSlowa[i].tlm, u = plikSlowa[i].caseSensit, w = str(plikSlowa[i].nextAnswDate)))
        n = 0
    try:   
        while n == 0:
            print('Podaj numer pary, którą chcesz edytować: ')
            odp = int(input())

            odp1 = str(input('Podaj nowe słowo:'))
            plikSlowa[odp].slw = odp1
            odp1 = str(input('Podaj nowe tłumaczenie:'))
            plikSlowa[odp].tlm = odp1
            odp1 = bool(str(input('Podaj nową wartość parametru Case Sensitive (True lub False) Oznacza to czy program będzie brał pod uwagę wielkość liter (True) czy nie (False):')))
            plikSlowa[odp].caseSensit = odp1
            print('Podaj nową datę następnej odpowiedzi:')
            odp1 = int(input('Rok:'))
            odp2 = int(input('Miesiąc:'))
            odp3 = int(input('Dzień:'))
            plikSlowa[odp].nextAnswDate = dt.date(odp1,odp2,odp3)
            
            print('''Czy chcesz edytować kolejną parę słów?
Tak - Y
Nie - N''')
            odp = str(input()).lower()
            if odp == 'n':
                print('Przechodzimy do zapisu zmodyfikowanego pliku')
                zapisz_liste(plikSlowa)
                print('Zmodyfikowany plik został zapisany.')
                return plikSlowa
                n = 1
    except:
        print('Coś poszło nie tak! Następnym razem dokładnie stosuj się do instrukcji! Zamykam program.')
        sys.exit('')
    
    
    
    
    

def main():
    print('Witaj w programie do nauki słówek!')
    print('''Czy masz już plik z słowami do nauki?
Tak - Y
Nie - N''')
    odp = str(input()).lower()
    
    if odp == 'y':
        glownaListaSlow = wczytaj_liste()
        print('''Wybierz co chcesz zrobić dalej:
1 - Dodaj nowe słowa do pliku
2 - Zacznij naukę
3 - Edytuj plik''')
        odp2 = str(input())
        
        if odp2 == '1':
            glownaListaSlow = dodaj_słówka(glownaListaSlow)
            print('''Wybierz co chcesz zrobić dalej:
1 - Zacznij naukę
2 - Wyjdź z programu''')
            odp3 = str(input())
            
            if odp3 == '1':
                odpytuj(glownaListaSlow)
            elif odp3 == '2':
                sys.exit('')
            else:
                print('Wprowadziłeś niepoprawną odpowiedź, zamykam program.')
                sys.exit('')
        
        elif odp2 == '2':
            odpytuj(glownaListaSlow)
        
        elif odp2 == '3':
            glownaListaSlow = modyfikuj(glownaListaSlow)
            print('''
                  Wybierz co chcesz zrobić dalej:
1 - Zacznij naukę
2 - Wyjdź z programu''')
            odp3 = str(input())
            
            if odp3 == '1':
                odpytuj(glownaListaSlow)
            elif odp3 == '2':
                sys.exit('')
            else:
                print('Wprowadziłeś niepoprawną odpowiedź, zamykam program.')
                sys.exit('')
            
        else:
            print('Wprowadziłeś niepoprawną odpowiedź, zamykam program.')
            sys.exit('')
    
    elif odp == 'n':
        print('Przechodzę do tworzenia nowego pliku')
        glownaListaSlow = nowa_lista()
        print('Przechodzę do zapisywania nowej listy')
        zapisz_liste(glownaListaSlow)
        print('''Czy chcesz rozpocząć naukę?
Tak - Y
Nie - N''')
        odp3 = str(input()).lower()
        
        if odp3 == 'y':
            odpytuj(glownaListaSlow)
        elif odp3 == 'n':
            print('Wyłączam program.')
            sys.exit('')
        else: 
            print('Wprowadziłeś niepoprawną odpowiedź, zamykam program.')
            sys.exit('')
    else:
        print('Wprowadziłeś niepoprawną odpowiedź, zamykam program.')
        sys.exit('')
            
if __name__ == '__main__':
    main()
    