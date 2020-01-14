# -*- coding: utf-8 -*-
import mmap
import re
import os

from tokenizer.spanish.common_tokens import Conjunciones, Determinants, Preposiciones, Pronoun, Puntuation

script_dir = os.path.dirname(__file__)


class SpanishTokenizer(object):
    # TODO apply version system
    def __init__(self):
        self.f = open(script_dir + "/diccionario.txt")
        self.simplified_dictionary = open(script_dir + "/diccionario_sin_acento.txt")
        self.known_symbols = {
            Conjunciones, Determinants, Preposiciones, Pronoun, Puntuation
        }

    # Takes a word and returns a string
    def tokenize(self, word):
        word = word.lower()
        kw = self.known_word(word)
        if kw != -1:
            return kw
        else:
            d = self.search_in_dic(word, self.f)
            if d != -1:
                return d
            else:
                # if it's not in the usual words, we have a second chance
                dc = self.doblecheck(word)
                if dc != -1:
                    return dc
                else:
                    return word

    def search_in_dic(self, word, f):
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        i = s.find(("->" + word + '.').encode("utf-8"))
        if i != -1:
            return self.get_token_from(s, i)
        else:
            i = s.find(("->" + word + " (1).").encode("utf-8"))
            if i != -1:
                return self.get_token_from(s, i)
            else:
                i = s.find(("->" + word + ',').encode("utf-8"))
                #TODO try both genders
                if i != -1:
                    return self.get_token_from(s, i)
                else:
                    return -1

    # seeks the position i in mmaped s for the token
    @staticmethod
    def get_token_from(s, i):
        s.seek(i)
        definicion = s.readline()
        search = re.search("[0-9]\\. \\w*", str(definicion))
        if search is not None:
            return search.group(0)[3:]
        else:
            return -1

    def known_word(self, word):
        for tokenizer in self.known_symbols:
            t = tokenizer().tokenize(word)
            if t != -1:
                return t
        return -1

    ## Toma un posible verbo y devuelve la busqueda en diccionario terminado en ar er o ir
    def try_conjugador_inverso(self, word):
        conjugacion = {
            # AM-AR TOM-AR LIMPI-AR
            'ar': {
                #         YO   TU    EL   NOS     VOS    ELLOS
                'pres': {
                    '1ra': {'o', 'amos'},
                    '2da': {'ás', 'ais'},
                    '3ra': {'a', 'án'}
                },
                'pret-imp': {
                    '1ra': {'aba', 'ábamos'},
                    '2da': {'abas', 'abais'},
                    '3ra': {'aba', 'aban'}
                },
                'pret-per': {
                    '1ra': {'é', 'amos'},
                    '2da': {'aste', 'asteis'},
                    '3ra': {'ó', 'aron'}
                },
                'fut': {
                    '1ra': {'aré', 'aremos'},
                    '2da': {'arás', 'aréis'},
                    '3ra': {'ará', 'arán'}
                },
                'subj': {
                    '1ra': {'e', 'emos'},
                    '2da': {'es', 'éis'},
                    '3ra': {'en'}
                },
                'part': {
                    '': {'ado', 'ada'},
                },
                'ger': {
                    '': {'ando'}
                }
            },
            # CORRER EJERCER ROMPER PODER
            'er': {
                #         YO   TU    EL   NOS     VOS    ELLOS
                'pres': {
                    '1ra': {'o', 'emos'},
                    '2da': {'es', 'eis'},
                    '3ra': {'e',  'en'}
                },
                'pret-imp': {
                    '1ra': {'ía', 'íamos'},
                    '2da': {'ías', 'íais'},
                    '3ra': {'ía', 'ían'}
                },
                'pret-per': {
                    '1ra': {'í', 'iamos'},
                    '2da': {'iste', 'isteis'},
                    '3ra': {'ió', 'ieron'}
                },
                'fut': {
                    '1ra': {'eré', 'eremos'},
                    '2da': {'erás', 'eréis', },
                    '3ra': {'erá', 'rá', 'erán'}
                },
                'subj': {
                    '1ra': {'iera', 'ieramos'},
                    '2da': {'ieras', 'ierais'},
                    '3ra': {'ieran'}
                },
                'part': {
                    '': {'ido', 'ida'},
                },
                'ger': {
                    '': {'endo', 'iendo'}
                }
            },
            # ABRIR CURTIR SALIR
            'ir': {
                #         YO   TU    EL   NOS     VOS    ELLOS
                'pres': {
                    '1ra': {'o', 'imos'},
                    '2da': {'es', 'eis'},
                    '3ra': {'e', 'en'}
                },
                'pret-imp': {
                    '1ra': {'ía', 'íamos'},
                    '2da': {'ías', 'íais'},
                    '3ra': {'ía', 'ían'}
                },
                'pret-per': {
                    '1ra': {'í', 'iamos'},
                    '2da': {'iste', 'isteis'},
                    '3ra': {'ió', 'ieron'}
                },
                'fut': {
                    '1ra': {'iré', 'iremos'},
                    '2da': {'irás', 'iréis'},
                    '3ra': {'irá', 'irán'}
                },
                'subj': {
                    '1ra': {'a', 'amos'},
                    '2da': {'as', 'ais'},
                    '3ra': {'an'}
                },
                'part': {
                    '': {'ido'}
                },
                'ger': {
                    '': {'iendo'}
                }
            }
        }

        for infinitivo, tiempos in conjugacion.items():
            for t, personas in tiempos.items():
                for p, sufijos in personas.items():
                    for i, sufijo in enumerate(sufijos):
                        if word.endswith(sufijo) or word.endswith(sufijo
                                                                  .replace('á', 'a')
                                                                  .replace('é', 'e')
                                                                  .replace('í', 'i')
                                                                  .replace('ó', 'o')
                                                                  .replace('ú', 'u')):
                            search = self.search_in_dic(word[:-len(sufijo)] + infinitivo, self.f)
                            if search != -1:
                                if i == 0:
                                    return "verb:" + t + ":" + p
                                else:
                                    return "verb:" + t + ":" + p + ":pl"
        return -1

    def doblecheck(self, word):
        # puede que sea un plural
        terminaciones_pl = {'s', 'es', 'as'}
        for t in terminaciones_pl:
            if word.endswith(t):
                w = word[:-len(t)]
                d = self.search_in_dic(w, self.f)
                if d != -1:
                    return d+":pl"
        # capaz esta mal acentuada?
        d = self.search_in_dic(word, self.simplified_dictionary)
        if d != -1:
            return d
        # o capaz es un verbo conjugado
        tci = self.try_conjugador_inverso(word)
        if tci != -1:
            return tci
        # capaz es un verbo terminado en reflexivo
        ref = {'les', 'le', 'la', 'lo', 'los', 'las', 'te', 'me', 'se', 'sela', 'selo', 'selos', 'selas', 'sele',
               'seles'}
        for r in ref:
            if word.endswith(r):
                w = word[:-len(r)]
                d = self.search_in_dic(w, self.f)
                if d != -1:
                    return d + ":" + r
                d = self.search_in_dic(w, self.simplified_dictionary)
                if d != -1:
                    return d + ":" + r
                tci = self.try_conjugador_inverso(w)
                if tci != -1:
                    return tci + ":" + r
        return -1
