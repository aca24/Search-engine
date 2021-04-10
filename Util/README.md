# **_SEARCH ENGINE_**

### OSNOVNE INFORMACIJE O PROJEKTU


- Programski jezik: Python 3
- Verzija: python-3.7.4-amd64-webinstall
- Importi koji su korišćeni:

1. Import os - koristi se za potrebe prolaska kroz zadate putanje
  

OBAVEŠTENJE: Ukoliko koristite Linux operativni sistem, u 'myParser.py' potrebno je izmeniti 72. liniju koda i 
umesto encoding="utf-8" staviti 'r', jer parser za sve dokumente vrati određen broj reči.
Ukoliko koristite Windows operativni sistem parser može da vrati za neke dokumente 0 reči i zbog toga treba ostaviti
u 72. liniji encoding="utf-8".


#### KRATAK OPIS:

- Projekat je napravljen u svrhu potrebe predmeta "Osnovi informacionih sistema i softverskog inženjerstva".
- Predstavlja  mašinu za pretraživanje tekstualnih dokumenata tj. **search engine** prevedeno na engleski.
- Program prilikom pokretanja obilazi stablo direktorijuma u datotečkom sistemu počevši od datog korena, 
 parsira tekstualne datoteke u njima i izgrađije strukture podataka potrebne za efikasno pretraživanje.
- Nakon toga, program omogućuje korisniku da unosi tekstualne upite koji se sastoje od jedne ili više reči 
razdvojenih razmakom, pretražuje dokumente koristeći prethodno kreirane strukture podataka i korisniku ispisuje 
rangirane rezultate pretrage u vidu putanja do dokumenata.

### RASPOEDELA ZADATAKA PO STUDENTIMA

#### _STUDENT 1 - Stefan Savić RA75-2017_

##### Funkcionalnosti  koje treba da implementira:
1. Parsiranje skupa HTML dokumenata - izgraditi trie stablo u koje će biti smeštene
sve reči iz svih HTML dokumenata.
2. Unos upita - parsiranje upita, određivanje reči i utvrđivanje postojanja nekog od
logičkih operatora AND, OR, odnosno NOT.
3. Pretraga dokumenata - određivanje skupova HTML stranica koje sadrže pojedinačne reči upita.
4. Osnovne skupovne operacije - primena osnovnih skupovnih operacija preseka, unije, odnosno 
komplementa i utvrđivanje rezultujućeg skupa stranica.

###### Strukture podataka:
1. Trie - pored odgovarajućih klasa kojima će se predstaviti trie stablo, potrebno je implementirati 
funkcije za dodavanje reči u stablo, odnosno pretragu reči u stablu.


#### _STUDENT 2 - Aleksandar Savić RA83-2017_
##### Funkcionalnosti  koje treba da implementira:
1. Parsiranje skupa HTML dokumenata - izgraditi graf u kome su čvorovi predstavljeni HTML stranicama, 
a grane predstavljene linkovima između HTML stranica.
2. Rangirana_pretraga – za sve stranice rezultujućeg skupa HTML stranica odrediti rang.
3. Prikaz rezultata - na osnovu prethodno određenog ranga, neophodno je sortirati stranice samostalno 
implementiranim optimalnim algoritmom za sortiranje. Prikazati putanje do ovako sortiranih stranica i 
navesti rang svake.
4. Paginacija rezultata – prikaz N stranica odjednom, kao i mogućnost kretanja napred odnosno nazad 
za N stranica. Korisniku dati mogućnost da dinamički promeni N.

###### Strukture podataka:
1. Graph - implementirati operacije za dodavanje HTML stranice u graf, nakon čega je neophodno povezati 
odgovarajuće čvorove grafa u skladu sa ulaznim, odnosno izlaznim linkovima.
2. Set - implementirati operacija za uniju, presek i komplement skupa
