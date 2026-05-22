# Relatório de Análise de Acidentes de Trânsito - 2025

**Data de geração:** 22/05/2026 13:21:16  
**Arquivo analisado:** `dados_tratados.csv`

---

## 1. Objetivo

Este relatório documenta o processo de carregamento, tratamento, análise, divisão em treino e teste, e visualização dos dados de acidentes de trânsito.

---

## 2. Metodologia

### 2.1 Carregamento dos dados
O arquivo CSV foi lido com:
- separador `;`
- codificação `latin1`

### 2.2 Teste exploratório
Foram executadas análises iniciais para validar a estrutura do dataset:
- visualização das primeiras linhas
- inspeção das colunas
- soma e média de `mortos` por estado
- agrupamento por estado e sexo

### 2.3 Tratamento dos dados
Foram aplicadas as seguintes regras:
- seleção das colunas úteis: `uf`, `sexo`, `mortos`, `causa_acidente`, `data_inversa`
- remoção de registros com `sexo = "Não Informado"` e `sexo = "Ignorado"`
- conversão da coluna `data_inversa` para data
- criação da coluna `mes`
- criação da coluna `regiao`
- exclusão de valores nulos

### 2.4 Separação em treino e teste
Os dados foram divididos em dois conjuntos:
- treino
- teste

### 2.5 Visualização dos dados
Foram gerados três gráficos principais e dois gráficos da etapa de treino/teste.

---

## 3. Resultado da Execução

### 3.1 Resumo numérico
- **Linhas originais:** 490955
- **Linhas após tratamento:** 490955
- **Linhas removidas:** 0
- **Percentual mantido:** 100.00%

### 3.2 Colunas
- **Colunas originais:** uf, sexo, mortos, causa_acidente, data_inversa, mes, regiao
- **Colunas tratadas:** uf, sexo, mortos, causa_acidente, data_inversa, mes, regiao

---

## 4. Gráficos Gerados

### 4.1 Envolvidos por Estado e Sexo

![Envolvidos por Estado e Sexo](saida_relatorio\grafico_sexo_por_estado.png)

### 4.2 Top 10 Causas de Acidentes

![Top 10 Causas de Acidentes](saida_relatorio\grafico_top_10_causas.png)

### 4.3 Boxplot Região x Mês

![Boxplot Região x Mês](saida_relatorio\grafico_boxplot.png)

---

## 5. Top 10 Causas de Acidentes

| Causa do acidente | Quantidade |
|---|---:|
| Reação tardia ou ineficiente do condutor | 69854 |
| Ausência de reação do condutor | 61438 |
| Velocidade Incompatível | 43729 |
| Acessar a via sem observar a presença dos outros veículos | 37287 |
| Condutor deixou de manter distância do veículo da frente | 34946 |
| Manobra de mudança de faixa | 26596 |
| Ingestão de álcool pelo condutor | 22939 |
| Transitar na contramão | 19159 |
| Ultrapassagem Indevida | 15622 |
| Condutor Dormindo | 14053 |

---

## 6. Mês com Mais Acidentes por Região

| Região | Mês | Quantidade |
|---|---:|---:|
| Centro-Oeste | 12 | 7108 |
| Nordeste | 6 | 10222 |
| Norte | 12 | 4105 |
| Sudeste | 12 | 13338 |
| Sul | 12 | 12485 |

---

## 7. Conclusão

O script foi executado com sucesso.
