class Graf:

    class Cvor:

        def __init__(self, fajlPutanja, veze):
            self.fajlPutanja = fajlPutanja
            self.veze = veze
            self.izlazni = []
            self.ulazni = []

        def dodajIzlazni(self, linkovan_cvor):
            self.izlazni.append(linkovan_cvor)

        def dodajUlazni(self, ulazniCvor):
            self.ulazni.append(ulazniCvor)

    def __init__(self):
        self.cvorovi = {}

    def dodajCvor(self, fajlPutanja, veze):
        self.cvorovi[fajlPutanja] = self.Cvor(fajlPutanja, veze)

    def poveziCvorove(self):
        for cvor in self.cvorovi.values():
            for link in cvor.veze:
                try:
                    cvor.dodajIzlazni(self.cvorovi[link])
                except:
                    print('Pokusavate da iz fajla ' + cvor.fajlPutanja + ' linkujete fajl ' +
                          link + ' koji nije pronadjen za vreme parsiranja')
                    continue
                self.cvorovi[link].dodajUlazni(cvor)
