import os
from base_conhecimento import BaseConhecimento
from assistente import Assistente, ler_inteiro

PASTA = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(PASTA, "data")


def main():
    base = BaseConhecimento(os.path.join(DATA, "base_conhecimento.json"))
    if not base.carregar():
        print("Não foi possível carregar a base de conhecimento. Encerrando com segurança.")
        return

    assistente = Assistente("Citizen Assist AI", base,
                            os.path.join(DATA, "historico.json"),
                            os.path.join(DATA, "atendimentos.csv"))

    print(f"\n=== {assistente.nome} ===")
    print("Orientações para pessoas idosas, com fonte e data de verificação.")
    print("Aviso: este assistente NÃO é um canal oficial.")
    print("Não digite CPF, telefone ou e-mail.")

    while True:
        print("\nMENU")
        print("  1. Fazer uma pergunta")
        print("  2. Navegar por categorias")
        print("  3. Ver indicadores")
        print("  4. Exportar atendimentos para CSV")
        print("  0. Sair")
        op = ler_inteiro("Escolha: ", 0, 4)
        if op == 1:
            assistente.perguntar()
        elif op == 2:
            assistente.navegar()
        elif op == 3:
            assistente.mostrar_indicadores()
        elif op == 4:
            assistente.exportar_csv()
        else:
            assistente.pedir_nota()
            assistente.exportar_csv()
            print("Até logo!")
            break


if __name__ == "__main__":
    main()
