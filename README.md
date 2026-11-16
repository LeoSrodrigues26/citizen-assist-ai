# Citizen Assist AI

Assistente de terminal que orienta **pessoas idosas** sobre saúde, direitos, benefícios e proteção, usando só uma base de conhecimento verificada (sem coletar dados pessoais).

## Integrantes
- Nome – RM
- Nome – RM

## Público e problema
(Explique com suas palavras: pessoas idosas perdem tempo para descobrir onde e como acessar serviços e direitos...)

## ODS relacionados
(Ex.: ODS 3 – Saúde e Bem-Estar; ODS 10 – Redução das Desigualdades; ODS 16 – Instituições Eficazes)

## Como executar
```
python main.py
```
Sem bibliotecas externas. Python 3.8+.

## Regra de pontuação
- Palavra-chave da orientação que aparece na pergunta: **+3**
- Palavra da pergunta (4+ letras) que aparece no título: **+1**
- 6 pontos ou mais: confiança **ALTA** | 3 a 5: **MÉDIA** | menos de 3: "não encontrei"
- Texto normalizado (minúsculas, sem acentos, sem pontuação) antes de comparar.

## Integrações com outras disciplinas
(Nenhuma / descreva)

## Fontes consultadas
- https://www.gov.br/saude
- https://www.gov.br/inss
- https://www.gov.br/mds
- https://www.gov.br/mdh
- https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm (Estatuto da Pessoa Idosa)

## Teste com usuários
- Pessoas de fora da equipe: (mín. 3) | Atendimentos: (mín. 10)
- Indicadores obtidos: (cole a saída da opção 3 do menu)
- Dúvidas sem solução: ...
- Melhoria feita a partir do teste: (ex.: nova palavra-chave "xxx" na orientação N)

## Limitações
- Busca por regras: não entende sinônimos que não estejam nas palavras-chave.
- Base com apenas 10 orientações; regras de algumas cidades (ex.: transporte) variam.
- Este assistente NÃO é um canal oficial.

## Vídeo técnico
(link do YouTube não listado)
