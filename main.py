import os

from OisisiProjekat2Python.Structures.Graf import Graf
from OisisiProjekat2Python.Structures.Set import MySet
from OisisiProjekat2Python.Util.myParser import Parser
from OisisiProjekat2Python.Util.parser_napredni import parsirajKomandu
from OisisiProjekat2Python.Util.queryEntry import SplitQuery
from OisisiProjekat2Python.Structures.trieTree import Trie


graf = Graf()


def main():
    while True:
        print("\nMENI BROJ 1 - OPCIJE:")
        print("0 - Prekid rada aplikacije")
        print("1 - Parisaranje skupa HTML dokumenata ")
        print("2 - Parser za naprednu pretragu ")

        unos = input()
        unos = unos.strip()

        #graf
        global graf

        if unos == "1":
            trieTree, vratiPrviMeni = parsiranjeSkupaHTMLDokumenata()  # vraca stablo

            graf.poveziCvorove()  #povezivanje cvorova

            if vratiPrviMeni is True:
                continue
            running = 1

            while running:
                print("\nMENI BROJ 2 - OPCIJE:")
                print("0 - Povratak na meni broj 1 gde možete odabrati putanju za parisaranje skupa HTML dokumenata")
                print("1 - Unos upita po kom ce se vršiti pretraga za prethodnu unetu putanju")


                print("Odaberite neku od ponuđenih opcija: ")
                temp = input()
                temp = temp.strip()
                if (temp.isnumeric()) is True:
                    number = int(temp)
                    if number <= 0:
                        print("!!! POVRATAK NA MENI BROJ 1 !!!")
                        running = 0
                    elif number <= 1:
                        queryEntry = SplitQuery()
                        print("\nOBAVEŠTENJE:"
                              "\n- Možete vršiti pretragu po AND, OR ili NOT operatoru ili pretragu bez operatora."
                              "\n- Ukoliko vršite pretragu po operatoru, operator se mora nalaziti između dve reči koje želite da pretaražite."
                              "\n- U pretrazi je dozvoljeno korišćenje isključivo jednog operatora."
                              "\n- Pretragu bez operatora možete vršite unosom jedne ili vise reči odvojenih razmakom."
                              "\n\nUnesite upit po kom želite da izvršite pretragu: ")

                        userInputTextForSplit = input()
                        userInputTextForSplit = userInputTextForSplit.strip()
                        listWithUserInputText = []
                        listWithUserInputText, logOp = queryEntry.split(userInputTextForSplit)

                        if listWithUserInputText is None:
                            print("PAŽNJA: Unesite ispravno! ")
                        else:  # ako sadrzi log i ako ne sadrzi
                            if logOp.__eq__("AND"):
                                print("\n*** Pretraga po AND operatoru ***")

                                ok1, number1, myDict1, path1 = trieTree.search(
                                    listWithUserInputText[0])  # prva rec
                                ok2, number2, myDict2, path2 = trieTree.search(
                                    listWithUserInputText[2])  # druga rec

                                # provera svih mogucih slucajeva
                                if ok1 is True and ok2 is True:
                                    # print("OBAVESTENJE: Obe reci koje ste uneli postoje.\n")

                                    rec1 = listWithUserInputText[0]
                                    rec2 = listWithUserInputText[2]

                                    # duplikati - provera
                                    if rec1 == rec2:
                                        # print("OBAVESTENJE: Unete reci za pretragu su iste!\n")
                                        myDict1[path1] = number1

                                        # poziv 3 funkcije za rangiranje,sortiranje i prikaz u page-iranje
                                        ocenjeneStranice = rangirajStranice(myDict1)
                                        QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                        prikazStranicaPageiranje(ocenjeneStranice)


                                        #zakomentarisao jer nije potrebno sa novim prikazom uz pageinaciju
                                        """
                                        mySet1 = MySet()
                                        for p in myDict1.keys():
                                            mySet1.addToSet(p)

                                        i = 1
                                        print("Rezultujuci skup:")
                                        for p in mySet1.pathsInSet.keys():
                                            print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict1[p])
                                            i += 1"""

                                    else:
                                        newDict = {}
                                        resultSet = MySet()
                                        mySet1 = MySet()
                                        mySet2 = MySet()

                                        myDict1[path1] = number1
                                        myDict2[path2] = number2

                                        for p in myDict1.keys():
                                            mySet1.addToSet(p)

                                        for p in myDict2.keys():
                                            mySet2.addToSet(p)

                                        resultSet.addToSet(path1)
                                        resultSet.addToSet(path2)
                                        resultSet = mySet1.intersection(mySet2)

                                        '''
                                        i = 1
                                        print("Rezultujuci skup:")
                                        for p in resultSet.pathsInSet.keys():
                                            if p in myDict1.keys() and p in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ",
                                                      myDict1[p] + myDict2[p])
                                                i += 1
                                            elif p in myDict1.keys() and p not in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict1[p])
                                                i += 1
                                            elif p not in myDict1.keys() and p in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict2[p])
                                                i += 1'''

                                        for p in resultSet.pathsInSet.keys():
                                            if p in myDict1.keys() and p in myDict2.keys():
                                                newDict[p] = myDict1[p] + myDict2[p]
                                            elif p in myDict1.keys() and p not in myDict2.keys():
                                                newDict[p] = myDict1[p]
                                            elif p not in myDict1.keys() and p in myDict2.keys():
                                                newDict[p] = myDict2[p]

                                        ocenjeneStranice = rangirajStranice(newDict)
                                        QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                        prikazStranicaPageiranje(ocenjeneStranice)

                                elif ok1 is True and ok2 is False:
                                    # vratim set samo za prvu rec
                                    print(
                                        "OBAVEŠTENJE: Reč pre 'AND' operatora koju ste uneli postoji, a posle 'AND' operatora ne postoji!")
                                    print(
                                        "             'AND' operator možete koristi isključivo ukoliko obe reči postoje!\n")
                                elif ok1 is False and ok2 is True:
                                    # vratim set samo za drugu rec
                                    print(
                                        "OBAVEŠTENJE: Reč posle 'AND' operatora koju ste uneli postoji, a pre 'AND' operatora ne postoji!")
                                    print(
                                        "             'AND' operator možete koristi isključivo ukoliko obe reči postoje!\n")
                                else:
                                    print(
                                        "OBAVEŠTENJE: Ne postoji nijedna reč koju ste uneli! Pokušajte ponovo da pretražite!\n")

                            elif logOp.__eq__("OR"):
                                print("\n*** Pretraga po OR operatoru ***")

                                ok1, number1, myDict1, path1 = trieTree.search(
                                    listWithUserInputText[0])  # prva rec
                                ok2, number2, myDict2, path2 = trieTree.search(
                                    listWithUserInputText[2])  # druga rec

                                # provera svih mogucih slucajeva
                                if ok1 is True and ok2 is True:
                                    # cuvaje poslednjeg brojaca i putanje u recnik
                                    # print("OBAVESTENJE: Obe reci koje ste uneli postoje.\n")

                                    rec1 = listWithUserInputText[0]
                                    rec2 = listWithUserInputText[2]

                                    if rec1 == rec2:

                                        # print("OBAVESTENJE: Unete reci za pretragu su iste!\n")
                                        myDict1[path1] = number1

                                        ocenjeneStranice = rangirajStranice(myDict1)
                                        QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                        prikazStranicaPageiranje(ocenjeneStranice)

                                        #zakomentarisao zbog novog ispisa
                                        """
                                        mySet1 = MySet()
                                        for p in myDict1.keys():
                                            mySet1.addToSet(p)

                                        i = 1
                                        print("Rezultujuci skup:")
                                        for p in mySet1.pathsInSet.keys():
                                            print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict1[p])
                                            i += 1"""

                                    else:
                                        newDict = {}
                                        resultSet = MySet()
                                        mySet1 = MySet()
                                        mySet2 = MySet()

                                        myDict1[path1] = number1
                                        myDict2[path2] = number2

                                        for p in myDict1.keys():
                                            mySet1.addToSet(p)

                                        for p in myDict2.keys():
                                            mySet2.addToSet(p)

                                        resultSet.addToSet(path1)
                                        resultSet.addToSet(path2)
                                        resultSet = mySet1.union(mySet2)

                                        # zakomentarisao zbog novog ispisa
                                        """i = 1
                                        print("Rezultujuci skup:")
                                        for p in resultSet.pathsInSet.keys():
                                            if p in myDict1.keys() and p in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ",
                                                      myDict1[p] + myDict2[p])
                                                i += 1
                                            elif p in myDict1.keys() and p not in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict1[p])
                                                i += 1
                                            elif p not in myDict1.keys() and p in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict2[p])
                                                i += 1"""

                                        for p in resultSet.pathsInSet.keys():
                                            if p in myDict1.keys() and p in myDict2.keys():
                                                newDict[p] = myDict1[p] + myDict2[p]
                                            elif p in myDict1.keys() and p not in myDict2.keys():
                                                newDict[p] = myDict1[p]
                                            elif p not in myDict1.keys() and p in myDict2.keys():
                                                newDict[p] = myDict2[p]

                                        ocenjeneStranice = rangirajStranice(newDict)
                                        QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                        prikazStranicaPageiranje(ocenjeneStranice)

                                elif ok1 is True and ok2 is False:
                                    # vratim set samo za prvu rec

                                    myDict1[path1] = number1

                                    ocenjeneStranice = rangirajStranice(myDict1)
                                    QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                    prikazStranicaPageiranje(ocenjeneStranice)

                                    # zakomentarisano zbog novog ispisa
                                    """
                                    mySet1 = MySet()
                                    for p in myDict1.keys():
                                        mySet1.addToSet(p)
                                    i = 1
                                    print("Rezultujuci skup:")
                                    for p in mySet1.pathsInSet.keys():
                                        print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict1[p])
                                        i += 1"""

                                elif ok1 is False and ok2 is True:
                                    # vratim set samo za drugu rec

                                    myDict2[path2] = number2

                                    ocenjeneStranice = rangirajStranice(myDict2)
                                    QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                    prikazStranicaPageiranje(ocenjeneStranice)

                                    """
                                    mySet2 = MySet()
                                    for p in myDict2.keys():
                                        mySet2.addToSet(p)

                                    i = 1
                                    print("Rezultujuci skup:")
                                    for p in mySet2.pathsInSet.keys():
                                        print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict2[p])
                                        i += 1"""
                                else:
                                    print(
                                        "OBAVEŠTENJE: Ne postoji nijedna reč koju ste uneli! Pokušajte ponovo da pretražite!\n")


                            elif logOp.__eq__("NOT"):
                                print("\n*** Pretraga po NOT operatoru ***")

                                ok1, number1, myDict1, path1 = trieTree.search(
                                    listWithUserInputText[0])  # prva rec
                                ok2, number2, myDict2, path2 = trieTree.search(
                                    listWithUserInputText[2])  # druga rec

                                # provera svih mogucih slucajeva

                                if ok1 is True and ok2 is True:
                                    # cuvaje poslednjeg brojaca i putanje u recnik
                                    # print("OBAVESTENJE: Obe reci koje ste uneli postoje.\n")

                                    rec1 = listWithUserInputText[0]
                                    rec2 = listWithUserInputText[2]

                                    if rec1 == rec2:
                                        print(
                                            "OBAVEŠTENJE: Unete reči za pretragu su iste! Rezultat pretrage je prazan skup!\n")
                                    else:
                                        newDict = {}
                                        resultSet = MySet()
                                        mySet1 = MySet()
                                        mySet2 = MySet()

                                        myDict1[path1] = number1
                                        myDict2[path2] = number2

                                        for p in myDict1.keys():
                                            mySet1.addToSet(p)

                                        for p in myDict2.keys():
                                            mySet2.addToSet(p)

                                        resultSet.addToSet(path1)
                                        resultSet.addToSet(path2)
                                        resultSet = mySet1.complement(mySet2)

                                        '''
                                        # Zakomentarisano zbog novog ispisa
                                        i = 1
                                        print("Rezultujuci skup:")
                                        for p in resultSet.pathsInSet.keys():
                                            if p in myDict1.keys() and p in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ",
                                                      myDict1[p] + myDict2[p])
                                                i += 1
                                            elif p in myDict1.keys() and p not in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ",
                                                      myDict1[p])
                                                i += 1
                                            elif p not in myDict1.keys() and p in myDict2.keys():
                                                print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ",
                                                      myDict2[p])
                                                i += 1'''

                                        for p in resultSet.pathsInSet.keys():
                                            if p in myDict1.keys() and p in myDict2.keys():
                                                newDict[p] = myDict1[p] + myDict2[p]
                                            elif p in myDict1.keys() and p not in myDict2.keys():
                                                newDict[p] = myDict1[p]
                                            elif p not in myDict1.keys() and p in myDict2.keys():
                                                newDict[p] = myDict2[p]

                                        ocenjeneStranice = rangirajStranice(newDict)
                                        QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                        prikazStranicaPageiranje(ocenjeneStranice)

                                elif ok1 is True and ok2 is False:

                                    myDict1[path1] = number1

                                    #rangiranje, sortiranje i ispis sa paginacijom
                                    ocenjeneStranice = rangirajStranice(myDict1)
                                    QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                    prikazStranicaPageiranje(ocenjeneStranice)

                                    """
                                    mySet1 = MySet()
                                    for p in myDict1.keys():
                                        mySet1.addToSet(p)
                                        
                                    i = 1
                                    print("Rezultujuci skup:")
                                    for p in mySet1.pathsInSet.keys():
                                        if p in myDict1.keys():
                                            print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict1[p])
                                            i += 1"""
                                elif ok1 is False and ok2 is True:
                                    print("OBAVEŠTENJE: Prva reč koju ste uneli ne postoji, a druga postoji!\n"
                                          "U toj situaciji NOT se posmatra kao unarni operator, a ne binarni!\n")
                                else:
                                    print(
                                        "OBAVEŠTENJE: Ne postoji nijedna reč koju ste uneli! Pokušajte ponovo da pretražite!\n")

                            else:
                                print("\n*** Pretraga BEZ logičkih operatora (po principu 'OR') ***\n")
                                # brisanje duplikata u listi
                                listWithUserInputText = list(dict.fromkeys(listWithUserInputText))

                                listLength = len(listWithUserInputText)

                                if listLength == 1:
                                    ok1, number1, myDict1, path1 = trieTree.search(listWithUserInputText[0])
                                    if ok1 is True:

                                        myDict1[path1] = number1

                                        #poziv 3 funkcije za rangiranje, sortiranje i prikaz u page-iranje
                                        ocenjeneStranice = rangirajStranice(myDict1)
                                        QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice)-1)
                                        prikazStranicaPageiranje(ocenjeneStranice)

                                        """
                                        mySet1 = MySet()
                                        
                                        for p in myDict1.keys():
                                            mySet1.addToSet(p)
                                            
                                        i = 1
                                        print("Rezultujuci skup:")
                                        for p in mySet1.pathsInSet.keys():
                                            print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", myDict1[p])
                                            i += 1"""
                                    else:
                                        print("OBAVEŠTENJE: Reč '", listWithUserInputText[0], "' ne postoji!")
                                else:

                                    newDict = {}
                                    resultSet = MySet()
                                    ok1, number1, myDict1, path1 = trieTree.search(listWithUserInputText[0])

                                    for i in range(0, listLength - 1):
                                        j = i + 1

                                        if j == 1:
                                            ok2, number2, myDict2, path2 = trieTree.search(listWithUserInputText[j])

                                            if ok1 is True and ok2 is True:

                                                mySet1 = MySet()
                                                mySet2 = MySet()

                                                myDict1[path1] = number1
                                                myDict2[path2] = number2

                                                for p in myDict1.keys():
                                                    mySet1.addToSet(p)

                                                for p in myDict2.keys():
                                                    mySet2.addToSet(p)

                                                resultSet.addToSet(path1)
                                                resultSet.addToSet(path2)
                                                resultSet = mySet1.union(mySet2)  # tu cuvam rezultat

                                                for p in resultSet.pathsInSet.keys():
                                                    if p in myDict1.keys() and p in myDict2.keys():
                                                        newDict[p] = myDict1[p] + myDict2[p]

                                                    elif p in myDict1.keys() and p not in myDict2.keys():
                                                        newDict[p] = myDict1[p]

                                                    elif p not in myDict1.keys() and p in myDict2.keys():
                                                        newDict[p] = myDict2[p]
                                            elif ok1 is True and ok2 is False:
                                                print("OBAVEŠTENJE: Reč '", listWithUserInputText[j], "' ne postoji!\n")
                                                resultSet = MySet()

                                                myDict1[path1] = number1
                                                for p in myDict1.keys():
                                                    resultSet.addToSet(p)

                                                for p in resultSet.pathsInSet.keys():
                                                    if p in myDict1.keys():
                                                        newDict[p] = myDict1[p]


                                            elif ok1 is False and ok2 is True:
                                                print("OBAVEŠTENJE: Reč '", listWithUserInputText[i], "' ne postoji!\n")
                                                resultSet = MySet()

                                                myDict2[path2] = number2
                                                for p in myDict2.keys():
                                                    resultSet.addToSet(p)

                                                for p in resultSet.pathsInSet.keys():
                                                    if p in myDict2.keys():
                                                        newDict[p] = myDict2[p]

                                            else:
                                                print("OBAVEŠTENJE: Reč '", listWithUserInputText[j], "' ne postoji!\n")
                                                print("OBAVEŠTENJE: Reč '", listWithUserInputText[i], "' ne postoji!\n")

                                        else:  # ako ima vise od 2 reci u pretrazi ulazi uvek u ovde
                                            ok2, number2, myDict2, path2 = trieTree.search(listWithUserInputText[j])

                                            if ok2 is True:
                                                mySet2 = MySet()

                                                myDict2[path2] = number2

                                                for p in myDict2.keys():
                                                    mySet2.addToSet(p)

                                                resultSet.addToSet(path2)
                                                resultSet = resultSet.union(mySet2)  # tu cuvam rezultat

                                                for p in resultSet.pathsInSet.keys():
                                                    if p in newDict.keys() and p in myDict2.keys():
                                                        newDict[p] = newDict[p] + myDict2[p]
                                                    elif p not in newDict.keys() and p in myDict2.keys():
                                                        newDict[p] = myDict2[p]
                                            elif ok2 is False:
                                                print("OBAVEŠTENJE: Reč '", listWithUserInputText[j], "' ne postoji!\n")

                                    # poziv 3 funkcije za rangiranje,sortiranje i prikaz u page-iranje
                                    ocenjeneStranice = rangirajStranice(newDict)
                                    QuickSort(ocenjeneStranice, 0, len(ocenjeneStranice) - 1)
                                    prikazStranicaPageiranje(ocenjeneStranice)


                                    """i = 1
                                    print("Rezultujuci skup:")
                                    for p in resultSet.pathsInSet.keys():

                                        if p in newDict.keys():
                                            print("PUTANJA BROJ ", i, ": ", p, " BROJ PONAVLJANJA: ", newDict[p])

                                            i += 1"""


                    else:
                        print("Pokušajte ponovo! Možete uneti samo neki od ponuđenih brojeva!")
                else:
                    print("Pokušajte ponovo! Možete uneti samo neki od ponuđenih brojeva!")
        elif unos == "2":
            print("\nOBAVESTENJE:"
                  "\n- Mozete vrsiti pretragu po &&, || ili ! operatoru ili pretragu bez operatora."
                  "\n- Operator && je AND, || OR a ! NOT."
                  "\n- Sada mozete koristiti reci and or i not u query-u posto nisu vise rezervisane komande")

            userInputTextForSplit = input()
            parsirajKomandu(userInputTextForSplit)
        elif unos == "0":
            print("!!! IZLAZAK IZ APLIKACIJE !!!")
            break
        else:
            print("Pokušajte ponovo! Možete uneti samo neki od ponuđenih brojeva!")


def parsiranjeSkupaHTMLDokumenata():
    print("\nPrimeri validnih putanja:")
    print("C:\\Users\\Stefan\\Desktop\\testZaProjekat\\test-skup")
    print("C:\\Users\\Stefan\\Desktop\\testZaProjekat\\c-api")
    print("C:\\Users\\Stefan\\Desktop\\testZaProjekat\\faq")
    print("\nUnesite putanju u kojoj želite da parsirate skup HTML dokumenata:")

    userInputPath = input()  # userInputPath - putanja koju korisnik unosi

    # graf
    global graf

    vratiPrviMeni = False
    userInputPath = userInputPath.strip()
    # pronasao validnu putanju
    pronasaoHTML = False
    # iz trieTree.py
    trieTree = Trie()
    # iz myParser.py
    parser = Parser()

    if userInputPath.strip().__eq__(""):
        print("Izaberite ponovo parisanje skupa HTML dokumenata, ali unestite validnu putanju!\
        \nNe sme biti prazan string!")
        vratiPrviMeni = True
        return trieTree, vratiPrviMeni

    # slucaj ukoliko se pojavi samo jedan html ili htm dokument
    if '.html' in userInputPath:
        print("Putanja je neodgovarajuća, jer ne predstavlja direktorijum (ne sme da sadrži '.html' u sebi)!")
        print("Ukoliko želite da izvršite parsiranje, unesite broj 1 i zatim unesite validnu putanju!")
        vratiPrviMeni = True
        return trieTree, vratiPrviMeni
    elif '.htm' in userInputPath:
        print("Putanja je neodgovarajuća, jer ne predstavlja direktorijum (ne sme da sadrži '.htm' u sebi)!")
        print("Ukoliko želite da izvršite parsiranje, unesite broj 1 i zatim unesite validnu putanju!")
        vratiPrviMeni = True
        return trieTree, vratiPrviMeni
    # ostali slucajevi
    else:
        for root, directories, files in os.walk(userInputPath):
            for file in files:
                # za svaki fajl koji sadrzi '.html' odradi posebno parsiranje
                if '.html' in file or '.htm' in file:
                    pronasaoHTML = True
                    parser.parse(os.path.join(root, file))  # jedan html fajl salje parseru

                    for word in parser.words:
                        trieTree.insertWord(word, os.path.join(root, file))


                    graf.dodajCvor(os.path.join(root, file), parser.links)



        if pronasaoHTML is False:
            print("Putanja koja je uneta ne sadrži \'.html\' ili \'.htm\' dokument! Unesite ispravnu putanju!")
            vratiPrviMeni = True
            return trieTree, vratiPrviMeni
        else:
            return trieTree, vratiPrviMeni


# funkcija za rangiranje
def rangirajStranice(myDict):
    global graf
    poeniDict = dict(myDict)
    for ime in myDict.keys():
        ulazniCvorovi = graf.cvorovi[ime].ulazni
        for cvor in ulazniCvorovi:
            if cvor.fajlPutanja in myDict:
                # ako se u cvoru pojavljuje neka rec, onda cvor vredi toliko koliko puta se ta rec pojavljuje
                poeniCvora = myDict[cvor.fajlPutanja]
            else:
                # ako se u cvoru ni jednom ne pojavljuje kljucna rec, onda taj cvor vredi 0.5 poena
                poeniCvora = 0.5
            # uzazli cvor dobija toliko poena koliko poena ima cvor koji linkuje na njega podeljeno sa ukupnim brojem
            # linkova
            poeniDict[ime] += poeniCvora / len(cvor.izlazni)

    # prebacujemo iz mape u listu, za lakse kasnije sortiranje
    poeniList = []
    for ime in poeniDict:
        poeniList.append([ime, poeniDict[ime]])
    return poeniList


#funkcija za sortiranje
def QuickSort(ocenjeneStranice, pocetniIndex, zavrsniIndex):

    if pocetniIndex >= zavrsniIndex:
        return
    pivot = partition(ocenjeneStranice, pocetniIndex, zavrsniIndex)
    QuickSort(ocenjeneStranice, pocetniIndex, pivot - 1)
    QuickSort(ocenjeneStranice, pivot + 1, zavrsniIndex)


#pomocna funkcija neophodna za QS
def partition(ocenjeneStranice, pocetniIndex, zavrsniIndex):

    index = pocetniIndex
    pivotniElement = ocenjeneStranice[zavrsniIndex]

    for i in range(pocetniIndex, zavrsniIndex):
        if ocenjeneStranice[i][1] >= pivotniElement[1]:
            temp = ocenjeneStranice[i]
            ocenjeneStranice[i] = ocenjeneStranice[index]
            ocenjeneStranice[index] = temp
            index += 1

    temp = ocenjeneStranice[zavrsniIndex]
    ocenjeneStranice[zavrsniIndex] = ocenjeneStranice[index]
    ocenjeneStranice[index] = temp
    return index

# pomocna funkcija za ispis, poziva se iz prikazStranicaPageiranje
def ispisiStranicu(n, broj_ispisanih_elemenata, niz):
    for i in range(0, n):
        if broj_ispisanih_elemenata + i < len(niz):
            print(str(broj_ispisanih_elemenata + i + 1) + '. ' + niz[broj_ispisanih_elemenata + i][0] + " " +
                  str(niz[broj_ispisanih_elemenata + i][1]))
        else:
            print('Nema vise stranica!')
            return True
    return False
    # ako vrati true, znamo da smo dosli do kraja niza, te nema smisla da pitamo korisnika da li hoce da mu prikazemo
    # sledecu stranicu, vec samo izlazimo iz funkcije
    # ako vrati true, znamo da smo dosli do kraja niza, te nema smisla da pitamo korisnika da li hoce da mu prikazemo
    # sledecu stranicu, vec samo izlazimo iz funkcije


# ispis uz page-iranje
def prikazStranicaPageiranje(niz):
    while True:
        n = input("Unesite zeljeni broj elemenata po stranici:\n")
        if n.isnumeric():
            break
        else:
            print("Unos mora biti broj")

    n = int(n)
    broj_ispisanih_elemenata = 0
    zavrsena = ispisiStranicu(n, broj_ispisanih_elemenata, niz)
    broj_ispisanih_elemenata += n
    if zavrsena:
        return

    while True:
        komanda = input("Unesite zeljenu akciju:\n"
                        "1 - Izlazak\n"
                        "2 - Sledeca strainca\n"
                        "3 - Prethodna stranica\n"
                        "4 - Promenite broj elemenata na jednoj stranici\n")
        if komanda == "1":
            break
        elif komanda == "2":
            zavrsena = ispisiStranicu(n, broj_ispisanih_elemenata, niz)
            broj_ispisanih_elemenata += n
            if zavrsena:
                return
        elif komanda == "3":
            if broj_ispisanih_elemenata == 0:
                print("Ovo je prva stranica!")
            else:
                broj_ispisanih_elemenata = max(0, broj_ispisanih_elemenata - 2*n)
                ispisiStranicu(n, broj_ispisanih_elemenata, niz)
                broj_ispisanih_elemenata += n
        elif komanda == "4":
            while True:
                n = input("Unesite zeljeni broj elemenata po stranici:\n")
                if n.isnumeric():
                    break
                else:
                    print("Unos mora biti broj")

            n = int(n)
            print("Promenili ste broj elemenata prikazanih na jednoj stranici na " + str(n))
        else:
            print("Nepoznata komanda.Pokusajte ponovo")


if __name__ == '__main__':
    main()