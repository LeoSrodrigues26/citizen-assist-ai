import csv
import json
import time
from datetime import datetime

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_s", "nota_facilidade"]


def ler_sn(mensagem):
    while True:
        r = input(mensagem).strip().lower()
        if r in ("s", "n"):
            return r == "s"
        print("Responda apenas com s ou n.")


def ler_inteiro(mensagem, minimo, maximo):
    while True:
        r = input(mensagem).strip()
        if r.isdigit() and minimo <= int(r) <= maximo:
            return int(r)
        print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")


class Assistente:
    def __init__(self, nome, base, caminho_historico, caminho_csv):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico = []
        self.carregar_historico()
        self.inicio_sessao = len(self.historico)

    # ---------- histórico ----------
    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arq:
                dados = json.load(arq)
            self.historico = dados if isinstance(dados, list) else []
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            self.historico = []

    def salvar_historico(self):
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as arq:
                json.dump(self.historico, arq, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar o histórico.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou,
                  ajudou, tentativas, tempo):
        self.historico.append({
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_s": tempo,
            "nota_facilidade": None,
        })
        self.salvar_historico()

    # ---------- dados pessoais ----------
    @staticmethod
    def tem_dado_pessoal(texto):
        digitos = sum(1 for c in texto if c.isdigit())
        return digitos >= 8 or "@" in texto

    # ---------- atendimento por pergunta ----------
    def perguntar(self):
        while True:
            inicio = time.time()
            tentativas = 0
            ultima = ""
            while True:
                texto = input("\nDigite sua dúvida (0 para voltar): ").strip()
                if texto == "0":
                    if tentativas > 0:  # tentou e não achou: dúvida sem solução
                        self.registrar("pergunta", ultima, None, False, False,
                                       tentativas, round(time.time() - inicio, 1))
                    return
                if not texto:
                    print("Digite sua dúvida ou 0 para voltar.")
                    continue
                if self.tem_dado_pessoal(texto):
                    print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                    continue  # não registra

                tentativas += 1
                ultima = texto
                resultados = self.base.buscar(texto)
                if not resultados or resultados[0][0] < 3:
                    print("Não encontrei uma orientação para essa dúvida.")
                    print("Tente outras palavras (ex.: o nome do documento ou serviço)")
                    print("ou use a navegação por categorias no menu.")
                    continue

                pontos, melhor = resultados[0]
                print(f"\nConfiança da resposta: {self.base.confianca(pontos)} ({pontos} pontos)")
                melhor.exibir()
                alternativas = resultados[1:3]
                if alternativas:
                    print("\nVeja também:")
                    for p, o in alternativas:
                        print(f"  - {o.titulo} ({p} pontos)")

                ajudou = ler_sn("\nEssa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("pergunta", texto, melhor.id, True, ajudou,
                               tentativas, round(time.time() - inicio, 1))
                break  # fim do atendimento; começa outro

    # ---------- navegação por categorias ----------
    def navegar(self):
        while True:
            categorias = self.base.categorias()
            print("\nCategorias:")
            for i, c in enumerate(categorias, 1):
                print(f"  {i}. {c}")
            print("  0. Voltar")
            op = ler_inteiro("Escolha: ", 0, len(categorias))
            if op == 0:
                return
            categoria = categorias[op - 1]
            self._listar_categoria(categoria)

    def _listar_categoria(self, categoria):
        itens = self.base.por_categoria(categoria)
        while True:
            print(f"\n{categoria}:")
            for i, o in enumerate(itens, 1):
                print(f"  {i}. {o.titulo}")
            print("  0. Voltar")
            op = ler_inteiro("Escolha: ", 0, len(itens))
            if op == 0:
                return
            inicio = time.time()
            orientacao = itens[op - 1]
            orientacao.exibir()
            ajudou = ler_sn("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("categoria", categoria, orientacao.id, True, ajudou,
                           1, round(time.time() - inicio, 1))

    # ---------- indicadores ----------
    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            return None
        encontrados = [h for h in self.historico if h["encontrou"]]
        ajudaram = [h for h in self.historico if h["ajudou"]]
        notas = [h["nota_facilidade"] for h in self.historico if h.get("nota_facilidade")]
        sem_solucao = [h["pergunta"] for h in self.historico
                       if (not h["encontrou"] or not h["ajudou"]) and h["origem"] == "pergunta"]
        return {
            "total": total,
            "encontrada_pct": round(100 * len(encontrados) / total, 1),
            "acerto_pct": round(100 * len(ajudaram) / total, 1),
            "tempo_medio": round(sum(h["tempo_s"] for h in encontrados) / len(encontrados), 1) if encontrados else 0,
            "tentativas_media": round(sum(h["tentativas"] for h in self.historico) / total, 1),
            "facilidade_media": round(sum(notas) / len(notas), 1) if notas else None,
            "sem_solucao": sem_solucao,
        }

    def mostrar_indicadores(self):
        ind = self.indicadores()
        if ind is None:
            print("Ainda não há atendimentos registrados.")
            return
        print("\n=== Indicadores ===")
        print(f"Atendimentos: {ind['total']}")
        print(f"Resposta encontrada (%): {ind['encontrada_pct']}")
        print(f"Taxa de acerto: ajudou (%): {ind['acerto_pct']}")
        print(f"Tempo médio para encontrar: {ind['tempo_medio']} s")
        print(f"Tentativas por atendimento: {ind['tentativas_media']}")
        fac = ind["facilidade_media"]
        print(f"Facilidade de uso (1 a 5): {fac if fac is not None else 'sem nota ainda'}")
        print("Dúvidas sem solução:")
        if ind["sem_solucao"]:
            for d in ind["sem_solucao"]:
                print(f"  - {d}")
        else:
            print("  (nenhuma)")

    # ---------- CSV ----------
    def exportar_csv(self):
        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arq:
                escritor = csv.DictWriter(arq, fieldnames=CAMPOS_CSV, extrasaction="ignore")
                escritor.writeheader()
                for h in self.historico:
                    escritor.writerow(h)
            print(f"CSV exportado em {self.caminho_csv}")
        except OSError:
            print("Não foi possível exportar o CSV.")

    # ---------- saída ----------
    def pedir_nota(self):
        if len(self.historico) <= self.inicio_sessao:
            return
        nota = ler_inteiro("De 1 a 5, quão fácil foi usar o assistente? ", 1, 5)
        for h in self.historico[self.inicio_sessao:]:
            h["nota_facilidade"] = nota
        self.salvar_historico()
