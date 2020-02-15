library(tidyverse)
library(reshape2)
library(lubridate)

# Wczytujemy dane - dla każdego produktu mamy jeden plik, które opakujemy w listę zbiorów danych
# Plik inflacja będzie nam potrzebny później i tam zostanie wytłumaczony

dane = list.files(path = 'dane', pattern = '*.csv', full.names = TRUE)
lista_danych = list()

for (i in 1:length(dane)) {
  temp = read.csv(dane[[i]], sep = ';', na.strings = c('', '0,00'), stringsAsFactors = FALSE)
  lista_danych[[i]] = temp
}

inflacja = read.csv('WzrostCen.csv', sep = ';', na.strings = c(''), stringsAsFactors = FALSE)

ilosc_zbiorow = length(lista_danych)

# Porządkowanie wartości: konwertujemy wartości na klase numeric, usuwamy niepotrzebne kolumny i zmieniamy nazwy tym, które
# zostały. Usuwamy z każdego zbioru dane o całej Polsce, gdyż sami będziemy je liczyć.

lista_danych[[1]][[4]] = 'ogrzewanie za 1m2'
lista_danych[[2]][[4]] = 'ciepła woda za 1m3'
lista_danych[[3]][[4]] = 'cytryny za 1kg'
lista_danych[[4]][[4]] = 'jaja śwież (chów wolnowybiegowy) za 1szt'
lista_danych[[5]][[4]] = 'karp świeży za 1kg'
lista_danych[[6]][[4]] = 'piwo lager w butelce za 0,5l'
lista_danych[[7]][[4]] = 'podkoszulek męski bez rękawa'
lista_danych[[8]][[4]] = 'podkoszulek męski z krótkim rękawem'
lista_danych[[9]][[4]] = 'ser dojrzewający za 1kg'
lista_danych[[10]][[4]] = 'sok jabłkowy za 1l'
lista_danych[[11]][[4]] = 'ziemniaki za 1kg'


for (i in 1:ilosc_zbiorow) {
  lista_danych[[i]] = subset(lista_danych[[i]], select = -c(Kod, Cena.i.wskaźniki, Jednostka.miary, Atrybut, X))
  colnames(lista_danych[[i]]) <- c('Region', 'Miesiąc', 'Rodzaj towaru/usługi', 'Rok', 'Wartość')
}

for (i in 1:ilosc_zbiorow) {
  lista_danych[[i]] = transform(lista_danych[[i]], Wartość = as.numeric(sub(',','.',as.character(Wartość))))
  lista_danych[[i]] = lista_danych[[i]][ ! lista_danych[[i]]$Region %in% 'POLSKA',]
  rownames(lista_danych[[i]]) <- NULL
}

inflacja = subset(inflacja, select = -c(Kod, Grupy.towarów.i.usług, Jednostka.miary, Atrybut, X))
colnames(inflacja) <- c('Region', 'Rok', 'Wartość')
inflacja = transform(inflacja, Wartość = as.numeric(sub(',','.',as.character(Wartość))) / 100)

# brakujące dane cenowe koszulek bez rękawa uzupełnimy cenami koszulek z rękawem, następnie usuwamy zbędną listę i korygujemy
# argument ilosc_danych, robimy to by następna pętla for poprawnie działała i zajmowała mniej czasu

lista_danych[[7]]$Wartość[is.na(lista_danych[[7]]$Wartość)] = lista_danych[[8]]$Wartość[is.na(lista_danych[[7]]$Wartość)]
lista_danych[[8]] <- NULL
ilosc_zbiorow = length(lista_danych)

# Zgodnie z danymi gusu od marca do listopada ceny świeżego karpia są niemierzalne ze względu na wysoki błąd losowy próby w badaniach reprezentacyjnych
# brak informacji wiarygodnych lub porównywalnych. Z tego względu usuniemy te dane z naszego zbioru (wszędzie cena jest NA)
# Musimy też uzupełnić cenę w woj. Opolskim w lutym 2019 - zrobimy to używając mediany cen z lutego 2019 w pozostałych woj.

lista_danych[[5]] <- lista_danych[[5]][ ! lista_danych[[5]]$Miesiąc %in% c('marzec', 'kwiecień', 'maj', 'czerwiec', 'lipiec', 'sierpień', 'wrzesień','październik', 'listopad'),]
rownames(lista_danych[[5]]) = NULL

mediana = median(lista_danych[[5]]$Wartość[which(lista_danych[[5]]$Miesiąc %in% 'luty' & lista_danych[[5]]$Rok %in% 2019)], na.rm = TRUE)
lista_danych[[5]]$Wartość[322] = round(mediana, digits = 2)

# Mógłbym powyżej użyć funkcji which() zamiast 1372 ale wyrażenie zrobiłoby się 
# niezwykle długie - znalazłem ten indeks w konsoli za pomocą which()

# Uzupełniam brakujące ceny wartościami cen z lat przyszłych podzielonymi przez wartość inflacji
# Wzrost cen w roku 2013 w stosunku do 2012 w woj Zach-Pom = 100,9, gdzie 100 to taka sama cena
# W poprzednim kroku wszystkie wartości podzieliłem przez 100, więc mamy 1,009
# Czyli cena w 2013 = cena w 2012 * 1,009, zatem cena w 2012 = cena w 2013 / 1,009
# Puszczam pętlę, która w ten sposób uzupełnia wszystkie wartości, patrzy czy dana cena ma wartość czy nie i jeśli nie to
# Uzupełnia wartość ceną z przyszłego roku (nigdy nie brakuje cen w roku 2019, a w 2006 często - stąd ten wybór)
# Podzieloną przez wartość inflacji, sprwadzając w liście inflacji czy zgadza się region i rok, tak samo robi z cenami == 0
# Zaokrąglamy do 2 cyfr po przecinku

for (i in 1:ilosc_zbiorow) {
  for (j in length(lista_danych[[i]]$Wartość):1) {
    if (is.na(lista_danych[[i]]$Wartość[j]) == TRUE) {
      rok = lista_danych[[i]]$Rok[j]
      region = lista_danych[[i]]$Region[j]
      pozycja_inflacji = which(inflacja$Region %in% region & inflacja$Rok %in% rok)
      lista_danych[[i]]$Wartość[j] = lista_danych[[i]]$Wartość[j+1] / inflacja$Wartość[pozycja_inflacji]
      lista_danych[[i]]$Wartość[j] = round(lista_danych[[i]]$Wartość[j], digits = 2)
    }
  }
}

karp = lista_danych[[5]]
lista_danych[[5]] = NULL
ilosc_zbiorow = length(lista_danych)

#Tworzę folder WykresyCen, a w nim folder na każde województwo, w którym będę zapisywał wykresy

dir.create(paste(getwd(),'/WykresyCen', sep = ''))
for (woje in unique(lista_danych[[1]]$Region)) {
  dir.create(paste(getwd(),'/WykresyCen/',woje, sep = ''))
}

#Przechodzimy do tworzenia wykresów - dla każdego województwa powstają 3 wykresy ze względu na rozbierzność cen między 
#3 kategoriami produktów. Średnią cenę obliczam na podstawie średniej arytmetycznej ceny z każdego miesiąca w danym roku
#1 pętla for określa, który zbiór aktualnie będzie wykreślany na wykresie i określa wymagane parametry

for (podzial in c(1:3)) {
  if (podzial == 1) {
    nazwaPliku = 'ŚrednieCeny.part1.Wojewodztwo.'
    zakresDanych = c(2,6,7)
    skala = seq(10, 30, 2.5)
  } else if (podzial == 2) {
      nazwaPliku = 'ŚrednieCeny.part2.Wojewodztwo.'
      zakresDanych = 3
      skala = seq(4, 12, 1)
  } else {
    nazwaPliku = 'ŚrednieCeny.part3.Wojewodztwo.'
    zakresDanych = c(1,4,5,8,9)
    skala = seq(0, 5, 0.5)
  }
  
# W kolejnych pętlach for zbierane są dane potrzebne do wykreślenia wykresu

  for (wojew in unique(lista_danych[[1]]$Region)) {
    srCena = c()
    lata = c()
    produkty = c()

    for (i in zakresDanych) {
    podZbior = lista_danych[[i]][lista_danych[[i]]$Region %in% wojew,]

      for (rok in unique(podZbior$Rok)) {
        dane = podZbior[podZbior$Rok %in% rok,]
        sr = round(mean(dane$Wartość), digits = 2)
        lata = c(lata, rok)
        srCena = c(srCena, sr)
        produkty = c(produkty, lista_danych[[i]]$Rodzaj.towaru.usługi[1])
      }
    }


#Tworzenie wykresu i zapisywanie dzięki ggplot

    data = data.frame(produkty, lata, srCena)
    ggplot(data=data, aes(x=lata)) +
      scale_x_continuous(name = 'Rok', breaks = seq(2006, 2019, 1))+
      scale_y_continuous(name = 'Średnia cena w zł', breaks = skala)+
      geom_line(aes(y=srCena, col = produkty))+
      geom_point(aes(y=srCena, col = produkty),colour = 'royalblue', size = 2)+
      labs(title=paste('Średnia cena  wybranych produktów w latach 2006-2019'),
           subtitle=paste("Województwo", wojew)) +
      theme(legend.position = 'bottom',
            legend.key.size = unit(0.4, "cm"),
            legend.title = element_text(size = 12, face = "bold"),
            legend.text = element_text(size = 8)) +
    ggsave(paste(nazwaPliku,wojew, "png", sep="."), path = paste(getwd(),'/WykresyCen/',wojew, sep = ''), scale = 1.5)
  }
}

#Podobna pętla zmodyfikowana w celu wykreślenia danych dla całej Polski

dir.create(paste(getwd(),'/DanePolska', sep = ''))

for (podzial in c(1:3)) {
  
  srCena = c()
  lata = c()
  produkty = c()
  
  if (podzial == 1) {
    nazwaPliku = 'ŚrednieCeny.part1.Polska'
    zakresDanych = c(2,6,7)
    skala = seq(10, 30, 2.5)
  } else if (podzial == 2) {
    nazwaPliku = 'ŚrednieCeny.part2.Polska'
    zakresDanych = 3
    skala = seq(4, 12, 1)
  } else {
    nazwaPliku = 'ŚrednieCeny.part3.Polska'
    zakresDanych = c(1,4,5,8,9)
    skala = seq(0, 5, 0.5)
  }
  
  
  # W kolejnych pętlach for zbierane są dane potrzebne do wykreślenia wykresu
  
  for (i in zakresDanych) {
    

    
    for (rok in unique(lista_danych[[i]]$Rok)) {
      podZbior = lista_danych[[i]][lista_danych[[i]]$Rok %in% rok,]
        sr = round(mean(podZbior$Wartość), digits = 2)
        lata = c(lata, rok)
        srCena = c(srCena, sr)
        produkty = c(produkty, lista_danych[[i]]$Rodzaj.towaru.usługi[1])
      # for (wojew in unique(podZbior$Region)) {
      #   dane = podZbior[podZbior$Region %in% wojew,]
      #   sr = round(mean(dane$Wartość), digits = 2)
      #   lata = c(lata, rok)
      #   srCena = c(srCena, sr)
      #   produkty = c(produkty, lista_danych[[i]]$Rodzaj.towaru.usługi[1])
      # }
      
    }
  }
    
    #Tworzenie wykresu i zapisywanie dzięki ggplot
    
    data = data.frame(produkty, lata, srCena)
    ggplot(data=data, aes(x=lata)) +
      scale_x_continuous(name = 'Rok', breaks = seq(2006, 2019, 1))+
      scale_y_continuous(name = 'Średnia cena w zł', breaks = skala)+
      geom_line(aes(y=srCena, col = produkty))+
      geom_point(aes(y=srCena, col = produkty),colour = 'royalblue', size = 2)+
      labs(title=paste('Średnia cena wybranych produktów w latach 2006-2019'),
           subtitle= "W skali Polski") +
      theme(legend.position = 'bottom',
            legend.key.size = unit(0.4, "cm"),
            legend.title = element_text(size = 12, face = "bold"), 
            legend.text = element_text(size = 8)) +
      ggsave(paste(nazwaPliku, "png", sep="."), path = paste(getwd(),'/DanePolska', sep = ''), scale = 1.5)
   
}


#Najtańsze produkty w badanym okresie były w następujących miejscach w następującym czasie:

minimum = lista_danych[[1]][which(lista_danych[[1]]$Wartość %in% min(lista_danych[[1]]$Wartość)),][1,]

for (i in 2:ilosc_zbiorow) {
  minimum = rbind(minimum,lista_danych[[i]][which(lista_danych[[i]]$Wartość %in% min(lista_danych[[i]]$Wartość)),][1,])
}
print(minimum)

#Najdroższe produkty w badanym okresie były w następujących miejscach w następującym czasie:

maximum = lista_danych[[1]][which(lista_danych[[1]]$Wartość %in% max(lista_danych[[1]]$Wartość)),][1,]

for (i in 2:ilosc_zbiorow) {
  maximum = rbind(maximum,lista_danych[[i]][which(lista_danych[[i]]$Wartość %in% max(lista_danych[[i]]$Wartość)),][1,])
}
print(maximum)

#W Polsce wraz z upływem lat żyje się coraz drożej. Program 500+, który zaczął działać w 2016 roku ma różny wpływ na cenę,
#W zależności od produktu. Z tego względu na bazie tych danych nie jestem w stanie stwierdzić jaki miał wpływ na całokształt
#Cen.