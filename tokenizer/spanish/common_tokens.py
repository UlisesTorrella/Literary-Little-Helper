# -*- coding: utf-8 -*-
import re
from abc import ABC, abstractmethod


class CommonTokens(ABC):
    def tokenize(self, word):
        if word in self.known:
            return self.name + ":" + self.indentify(word)
        else:
            return -1
        
    @abstractmethod
    def indentify(self, word):
        pass


class Pronoun(CommonTokens):
    name = "pron"

    known = {"yo", "tú",   "usted", "ustedes", "vosotras",  "ellas", "él", "nosotros", "ellos",   "vosotros", "nosotras", "ella",
                  "mi", "mis", "mío", "mía", "míos", "mías", "tu", "tus", "tuyo", "tuya", "tuyos", "tuyas", "su", "sus", "suyo",
                  "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros",
                  "vuestras", "de", "que", "el", "la", "las", "lo", "los", "quien", "quienes", "el", "los", "la",
                    "las", "lo", "cuyo", "cuyos", "cuyas", "cuya", "donde", "con", "me", "te", "se", "nos", "os", "se"}

    personal = {"yo", "tú", "usted", "ustedes", "vosotras",  "ellas",
                "él", "nosotros", "ellos", "vosotros", "nosotras", "ella"}
    possessive = {"mi", "mis", "mío", "mía", "míos", "mías", "tu", "tus", "tuyo", "tuya", "tuyos",
                  "tuyas", "su", "sus", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra",
                  "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "de"}
    reflexive = {"que", "el", "la", "las", "lo", "los", "quien", "quienes", "el", "los", "la",
                  "las", "lo", "cuyo", "cuyos", "cuyas", "cuya", "donde", "con"}
    relative = {"me", "te", "se", "nos", "os", "se"}

    feminine = {"vosotras", "ellas", "nosotras", "ella", "mía", "mías", "tuya", "tuyas", "suya", "suyas",
                "nuestra", "nuestras", "vuestra", "vuestras", "la", "las", "las", "la", "cuyas", "cuya"}

    plural = {"ustedes", "vosotras",  "ellas", "nosotros", "ellos",   "vosotros", "nosotras", "mis", "míos",
              "mías", "tus", "tuyos", "tuyas", "sus", "suyos", "suyas", "nuestros", "nuestras", "vuestros",
                  "vuestras", "las", "los", "quienes", "los", "las", "cuyos", "cuyas", "nos", "os"}

    def indentify(self, word):
        if word in self.personal:
            return "per:" + self.gender(word) + ":" + self.person(word)
        if word in self.possessive:
            return "pos:" + self.gender(word) + ":" + self.person(word)
        if word in self.reflexive:
            return "ref:" + self.gender(word) + ":" + self.person(word)
        if word in self.relative:
            return "rel:" + self.gender(word) + ":" + self.person(word)

    def gender(self, word):
        if word in self.feminine:
            return "fem"
        else:
            return "mas"

    def person(self, word):
        if word in self.plural:
            return "plu"
        else:
            return "sing"


class Determinants(CommonTokens):
    name = "det"

    known = {"este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella", "aquellos", "aquellas",
             "un", "uno", "unos", "una", "unas", "alguno", "algunos", "cualquiera","ninguno", "pocos", "poco", "mucho",
             "muchos", "mucha", "muchas", "escaso", "escasos", "escasa", "escasas", "demasiado", "demasiada",
             "demasiados", "demasiadas", "bastantes", "bastante", "otro", "otros", "tanto", "tantos",  "todo", "todos",
             "vario", "varios", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
             "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve",
             "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien", "mil",
             "primero", "segundo", "tercero", "cuarto", "quinto", "sexto", "séptimo", "octavo", "noveno", "décimo",
             "undécimo", "duodécimo", "decimotercero", "decimocuarto", "vigésimo", "vigésimoprimero", "trigésimo",
             "cuadragésimo", "quincuagésimo", "sexagésimo", "septuagésimo", "octogésimo", "nonagésimo", "centésimo",
             "ducentésimo", "tricentésimo", "medio", "cuarto", "octavo", "doceavo", "doble", "triple", "cuádruple",
             "quíntuple", "séxtuple", "séptuple", "óctuple", "nónuplo", "décuplo", "undéclupo", "duodéclupo", "qué",
             "cuánto", "cuánta", "cuántos", "cuántas", "cuándo", "cuál", "cuáles", "dónde",  "otra", "otras", "tanta",
             "tantas", "toda", "todas", "varias"}

    demostrativo = {"este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel",
                "aquella", "aquellos", "aquellas"}
    indeterminado = {"un", "uno", "unos", "una", "unas", "alguno", "algunos", "cualquiera", "ninguno",
                "pocos", "poco", "mucho", "muchos", "escaso", "escasos", "demasiado",
                "demasiados", "bastantes", "bastante", "otro", "otros", "tanto", "tantos",
                "todo", "todos", "vario", "varios"}
    card = {"uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
                     "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis",
                     "diecisiete", "dieciocho", "diecinueve", "veinte", "treinta", "cuarenta",
                     "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien", "mil"}
    ord = {"primero", "segundo", "tercero", "cuarto", "quinto", "sexto", "séptimo",
                    "octavo", "noveno", "décimo", "undécimo", "duodécimo", "decimotercero",
                    "decimocuarto", "vigésimo", "vigésimoprimero", "trigésimo", "cuadragésimo",
                    "quincuagésimo", "sexagésimo", "septuagésimo", "octogésimo", "nonagésimo",
                    "centésimo", "ducentésimo", "tricentésimo"}
    frac = {"medio", "cuarto", "octavo", "doceavo"}
    mul = {"doble", "triple", "cuádruple", "quíntuple", "séxtuple", "séptuple",
                    "óctuple", "nónuplo", "décuplo", "undéclupo", "duodéclupo"}
    ivos = {"qué", "cuánto", "cuánta", "cuántos", "cuántas", "cuándo", "cuál", "cuáles",
                 "dónde"}

    feminine = {"esta", "estas", "esa", "esas", "aquella", "aquellas", "una", "unas", "cualquiera", "mucha", "muchas",
                "escasa", "escasas", "demasiada", "demasiadas", "otra", "otras", "tanta", "tantas",
                "toda", "todas", "varias", "cuánta", "cuántas", }

    plural = {"estos", "estas", "esos", "esas", "aquellos", "aquellas", "unos", "unas", "algunos", "pocos", "muchos",
              "muchas", "escasos", "escasas", "demasiados", "demasiadas", "bastantes", "otros", "tantos", "todos",
              "varios", "cuántos", "cuántas", "cuáles", "otras", "tantas", "todas", "varias"}

    def tokenize(self, word):
        if word in self.known or re.match("\\w*[0-9]\\w*", word) is not None:
            return self.name + ":" + self.indentify(word)
        else:
            return -1

    def indentify(self, word):
        if word in self.demostrativo:
            return "dem:" + self.gender(word) + ":" + self.person(word)
        if word in self.indeterminado:
            return "ind:" + self.gender(word) + ":" + self.person(word)
        if word in self.card or word in self.ord or word in self.frac or word in self.mul \
                or re.match("[0-9]*", word) is not None:
            return "num"
        if word in self.ivos:
            return "ivos:" + self.gender(word) + ":" + self.person(word)

    def gender(self, word):
        if word in self.feminine:
            return "fem"
        else:
            return "mas"

    def person(self, word):
        if word in self.plural:
            return "plu"
        else:
            return "sing"


class Conjunciones(CommonTokens):
    name = "conj"
    known = {"y", "e", "ni", "que", "pero", "mas", "aunque", "sino", "siquiera", "o", "u", "ora", "sea", "bien", "pues",
             "entonces", "como", "más", "si", "así", "luego", "conque", "para", "porque", "cuando", "mientras", "antes",
             "despues", "apenas"},

    def indentify(self, word):
        return word


class Preposiciones(CommonTokens):
    name = "pre"
    known = {"a", "ante", "bajo", "con", "de", "desde", "durante", "en", "entre", "excepto", "hacia", "hasta", "mediante",
             "para", "por", "salvo", "según", "sin", "sobre", "tras"}

    def indentify(self, word):
        return ""


class Puntuation(CommonTokens):
    name = "punt"
    known = {'.', ',', '/', ':', ';', "-", "*", "—", "–", "<s>", "</s>", '¿', '?', '¡', '!', '«', '»', '"', "'", '<',
             ">", "...", "…"}

    def indentify(self, word):
        return word
