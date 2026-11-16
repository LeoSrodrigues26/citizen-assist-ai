import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

CAMPOS = ["id", "categoria", "titulo", "palavras_chave", "resposta",
          "documentos", "onde", "fonte", "verificado_em"]


def normalizar(texto):
    """Minúsculas, sem acentos e sem pontuação, com espaço nas pontas."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        """Lê o JSON. Se faltar ou estiver corrompido, não trava o programa."""
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arq:
                dados = json.load(arq)
        except FileNotFoundError:
            print(f"Aviso: arquivo {self.caminho} não encontrado.")
            return False
        except (json.JSONDecodeError, OSError):
            print(f"Aviso: arquivo {self.caminho} está corrompido.")
            return False

        if not isinstance(dados, list):
            print("Aviso: formato inesperado na base de conhecimento.")
            return False

        for registro in dados:
            if isinstance(registro, dict) and all(c in registro for c in CAMPOS):
                self.orientacoes.append(Orientacao(**{c: registro[c] for c in CAMPOS}))
            else:
                print("Aviso: um registro inválido foi ignorado.")
        return len(self.orientacoes) > 0

    def categorias(self):
        lista = []
        for o in self.orientacoes:
            if o.categoria not in lista:
                lista.append(o.categoria)
        return lista

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """+3 por palavra-chave na pergunta; +1 por palavra (4+ letras) no título."""
        pergunta_n = normalizar(pergunta)
        titulo_n = normalizar(orientacao.titulo)
        pontos = 0
        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta_n:
                pontos += 3
        for palavra in pergunta_n.split():
            if len(palavra) >= 4 and f" {palavra} " in titulo_n:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        """Devolve lista de tuplas (pontos, orientacao), da maior para a menor."""
        resultados = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultados.append((pontos, o))
        resultados.sort(key=lambda t: t[0], reverse=True)
        return resultados

    @staticmethod
    def confianca(pontos):
        if pontos >= 6:
            return "ALTA"
        if pontos >= 3:
            return "MÉDIA"
        return None
