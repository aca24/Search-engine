# -*- coding: utf-8 -*-
import re
import os

from html.parser import HTMLParser


class Parser(HTMLParser):
    """
    Parser HTML dokumenata

    Upotreba:
        parser = Parser()
        parser.parse(FILE_PATH)
    """

    def handle_starttag(self, tag, attrs):
        """
        Metoda beleži sadržaj href atributa

        Poziv metode vrši se implicitno prilikom nailaska na tag
        unutar HTML fajla. Ukoliko je u pitanju anchor tag, beleži
        se vrednost href atributa.

        Argumenti:
        - `tag`: naziv taga
        - `attrs`: lista atributa
        """
        if tag == 'a':
            # typecast da izbegnem looping
            attrs = dict(attrs)
            link = attrs['href']

            # ignoriši spoljnje linkove i uzmi u obzir samo html fajlove
            if not link.startswith('http'):
                # ukloni sekciju iz linka
                hash_index = link.rfind('#')
                if hash_index > -1:
                    link = link[:hash_index]

                if link.endswith('html') or link.endswith('htm'):
                    relative_path = os.path.join(self.path_root, link)
                    link_path = os.path.abspath(relative_path)
                    self.links.append(link_path)

    def handle_data(self, data):
        """
        Metoda beleži pronađene reči

        Poziv metode vrši se implicitno prilikom nailaska na sadržaj
        HTML elemenata. Sadržaj elementa se deli u reči koje se beleže
        u odgovarajuću listu.

        Argument:
        - `data`: dobijeni sadržaj elementa
        """
        stripped_text = re.sub('[\W]', ' ', data).split()
        if stripped_text:
            self.words.extend(stripped_text)

    def parse(self, path):
        """
        Metoda učitava sadržaj fajla i prosleđuje ga parseru

        Argument:
        - `path`: putanja do fajla
        """
        self.links = []
        self.words = []

        try:
             with open(path, encoding="utf-8") as document: #  with open(path, 'r') as document:
                self.path_root = os.path.abspath(os.path.dirname(path))
                content = document.read()
                self.feed(content)

                # očisti duplikate
                self.links = list(set(self.links))

        except IOError as e:
            print(e)
        finally:
            return self.links, self.words
