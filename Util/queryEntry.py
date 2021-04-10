
class SplitQuery:

    def split(self, userInputTextForSplit):
        parts = userInputTextForSplit.split()

        listWithoutLogicalOperators = []
        listWithLogicalOperators1 = []

        # punjenje lista
        for part in parts:
            if part.upper() in ['AND', 'OR', 'NOT']:
                # ako sadrzi logicki operator
                listWithLogicalOperators1.append(part.upper())
            else:
                # ako ne sadrzi logicki operator
                listWithoutLogicalOperators.append(part.upper())

        # ako je prazna lista BEZ logickih operatora
        if len(listWithoutLogicalOperators) == 0:
            print("GREŠKA: Nemoguće je izvršiti pretragu!\n"
                  "        Primeri ispravnih pretraga: python and programming\n"
                  "                                    python or programming\n"
                  "                                    python not programming\n"
                  "                                    python\n"
                  "                                    python programming\n")
            return None, ""
        # ako nije prazna lista BEZ logickih operatora
        else:
            if len(listWithLogicalOperators1) == 0:
                    #print("OBAVESTENJE: Ne postoji logicki operator!")
                    return listWithoutLogicalOperators, ""
            else:
                # za AND, OR, NOT
                if len(parts) > 3 or len(listWithLogicalOperators1) > 1 or len(listWithoutLogicalOperators) == 1:
                    print("GREŠKA:")
                    if len(parts) > 3:
                        print("Postoji više od 3 reči u upitu koji ste uneli.\
                         \nDozvoljeno je 3 reči ukoliko koristite pretragu sa logičkim operatorom!")
                    if len(listWithLogicalOperators1) > 1:
                        print("Postoji više logičkih operatora, a dozvoljen je samo jedan!")
                    if len(listWithoutLogicalOperators) == 1:
                        print("Postoji samo jedna reč koja nije logički operator, dozvoljene su tačno dve reči!")
                    print("Primeri ispravnih pretraga: python and programming\n"
                          "                            python or programming\n"
                          "                            python not programming\n"
                          "                            python\n"
                          "                            python programming\n")
                    return None, ""
                else:
                    # ako nije prazna nijedna lista, gledam na kom mestu je logicki operator

                    operator = listWithLogicalOperators1[0].upper() # povecavanje zbog poredjenja

                    if operator.__eq__("AND"):

                        if parts[1].upper() not in ["AND"]:

                            print("GREŠKA: Logički operator sme biti samo između prve i treće reči u pretrazi.")
                            print("        Primeri ispravnih pretraga: python and programming\n"
                                  "                                    python or programming\n"
                                  "                                    python not programming\n"
                                  "                                    python\n"
                                  "                                    python programming\n")
                            return None, "AND"
                    elif operator.__eq__("OR"):

                        if parts[1].upper() not in ["OR"]:

                            print("GREŠKA: Logički operator sme biti samo između prve i treće reči u pretrazi.")
                            print("        Primeri ispravnih pretraga: python and programming\n"
                                  "                                    python or programming\n"
                                  "                                    python not programming\n"
                                  "                                    python\n"
                                  "                                    python programming\n")
                            return None, "OR"
                    elif operator.__eq__("NOT"):
                        if parts[1].upper() not in ["NOT"]:

                            print("GREŠKA: Logički operator sme biti samo između prve i treće reči u pretrazi.")
                            print("        Primeri ispravnih pretraga: python and programming\n"
                                  "                                    python or programming\n"
                                  "                                    python not programming\n"
                                  "                                    python\n"
                                  "                                    python programming\n")
                            return None, "NOT"


                    prvi = listWithoutLogicalOperators[0]
                    drugi = listWithLogicalOperators1[0]
                    treci = listWithoutLogicalOperators[1]

                    novaLista = []

                    novaLista.append(prvi)
                    novaLista.append(drugi)
                    novaLista.append(treci)

                    return novaLista, drugi
