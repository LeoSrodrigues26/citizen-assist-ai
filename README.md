# Citizen Assist AI

Assistente de terminal, feito em Python, que orienta **pessoas idosas** sobre saúde, direitos, benefícios e proteção. Ele responde dúvidas usando apenas uma base de conhecimento com fontes oficiais e data de verificação, mostra o nível de confiança da resposta e **não coleta dados pessoais**.

Projeto da Global Solution 2026.2 (desafio CitizenTech) – Pensamento Computacional e Automação com Python, FIAP.

## Integrantes
- Leonardo Soares – RM 572986
- Matheus Pimenta – RM 569400
- Lucas Seiji – RM 569673

## Público e problema
**Público:** pessoas idosas (60 anos ou mais) e seus familiares.

**Problema:** muitas pessoas idosas perdem tempo para descobrir como fazer o Cartão SUS, onde tomar vacina, como pedir a gratuidade no transporte ou a aposentadoria, ou a quem recorrer em caso de maus-tratos. A informação existe, mas está espalhada em vários sites, em linguagem técnica e misturada com páginas que parecem oficiais e não são, o que aumenta o risco de golpes.

**Solução:** um assistente que responde em linguagem simples, diz quais documentos levar e onde ir, mostra a fonte oficial e a data em que a informação foi conferida, e avisa quando não encontrou uma resposta, em vez de inventar.

## ODS relacionados
- **ODS 3 – Saúde e Bem-Estar:** orientações sobre Cartão SUS, vacinação e medicamentos gratuitos.
- **ODS 10 – Redução das Desigualdades:** facilita o acesso a direitos e benefícios por quem tem menos acesso à informação digital.
- **ODS 16 – Paz, Justiça e Instituições Eficazes:** informação confiável sobre serviços públicos e canal de denúncia (Disque 100).

## Como executar
Requisitos: Python 3.8 ou superior. Não usa bibliotecas externas.

```
git clone https://github.com/LeoSrodrigues26/citizen-assist-ai.git
cd citizen-assist-ai
python main.py
```

Menu do programa:
1. Fazer uma pergunta (texto livre)
2. Navegar por categorias
3. Ver indicadores
4. Exportar atendimentos para CSV
0. Sair (pede uma nota de facilidade de 1 a 5 e exporta o CSV)

## Estrutura do projeto
```
citizen-assist-ai/
├── README.md
├── main.py                 # menu principal
├── orientacao.py           # classe Orientacao
├── base_conhecimento.py    # classe BaseConhecimento + normalizar()
├── assistente.py           # classe Assistente
└── data/
    ├── base_conhecimento.json   # 10 orientações, 4 categorias
    ├── historico.json           # atendimentos registrados
    └── atendimentos.csv         # exportação dos atendimentos
```

### Classes (composição)
```
Assistente
└── base: BaseConhecimento
    └── orientacoes: [Orientacao, Orientacao, ...]
```
- **Orientacao:** guarda os dados de um registro do JSON e os exibe na tela (`exibir()`).
- **BaseConhecimento:** lê o JSON (`carregar()`), lista categorias (`categorias()`, `por_categoria()`), pontua (`pontuar()`) e busca (`buscar()`, que devolve uma lista de tuplas `(pontos, orientacao)`).
- **Assistente:** faz o atendimento (`perguntar()`, `navegar()`), guarda o histórico (`registrar()`), calcula indicadores (`indicadores()`) e exporta o CSV (`exportar_csv()`).

## Regra de pontuação
Antes de comparar, o texto passa por `normalizar()`: minúsculas, sem acentos e sem pontuação.

| Regra | Pontos |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 |

| Melhor pontuação | Resultado |
|---|---|
| 6 ou mais | Confiança **ALTA** |
| 3 a 5 | Confiança **MÉDIA** |
| menos de 3 | "Não encontrei": sugere outras palavras ou as categorias |

O assistente mostra a melhor orientação e até duas alternativas.

**Exemplo:** "Como faço o cartão do SUS?" → `cartao do sus` (+3) + `sus` (+3) + `cartao` no título (+1) = **7 pontos, confiança ALTA**.

## Regras de atendimento
- Entradas inválidas (opção fora da faixa, letras, resposta vazia, s/n inválido) nunca encerram o programa.
- Perguntas com 8 ou mais dígitos ou com `@` são recusadas e **não são registradas**.
- Toda resposta mostra fonte, data de verificação e o aviso "este assistente NÃO é um canal oficial".
- JSON ausente ou corrompido não trava o programa.

## Histórico e indicadores
Cada atendimento é salvo em `data/historico.json` com: data, origem (pergunta ou categoria), pergunta, id da orientação, se encontrou, se ajudou, tentativas, tempo em segundos e nota de facilidade. O programa calcula: resposta encontrada (%), taxa de acerto (%), tempo médio, tentativas por atendimento, facilidade de uso (1 a 5) e a lista de dúvidas sem solução. Os atendimentos são exportados para `data/atendimentos.csv` com `csv.DictWriter`.

## Integrações com outras disciplinas
Nenhuma. O projeto usa apenas Python puro, com a busca por pontuação baseada em regras.

## Fontes consultadas
- Ministério da Saúde: https://www.gov.br/saude
- INSS: https://www.gov.br/inss
- Ministério do Desenvolvimento e Assistência Social (MDS): https://www.gov.br/mds
- Ministério dos Direitos Humanos (MDH): https://www.gov.br/mdh
- Estatuto da Pessoa Idosa (Lei 10.741/2003): https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm

## Teste com usuários
Testado com **X pessoas** de fora da equipe, somando **Y atendimentos** (nenhum nome ou dado pessoal foi registrado).

| Indicador | Resultado |
|---|---|
| Resposta encontrada (%) | 88.9 |
| Taxa de acerto: ajudou (%) | 88.9 |
| Tempo médio para encontrar (s) | 23.3 s |
| Tentativas por atendimento | 1.1 |
| Facilidade de uso (1 a 5) | 5.0 |

**Dúvidas sem solução:**
- pergunta: Posso andar de ônibus de graça?

**Melhoria feita a partir do teste:**
- incluido a frase "onibus de graça" na **{base_conhecimento.json}**

## Limitações
- A busca é por regras: só entende palavras que estão nas palavras-chave ou no título, não entende sinônimos nem erros de digitação.
- A base tem apenas 10 orientações e não cobre todos os serviços.
- Algumas regras variam por cidade (por exemplo, transporte gratuito), e o assistente traz só a regra geral.
- As informações precisam ser reconferidas periodicamente nas fontes oficiais.
- Este assistente **NÃO é um canal oficial**.

## Vídeo técnico
https://youtu.be/KR_V4BHSea8
