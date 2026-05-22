import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from sklearn.model_selection import train_test_split


def carregarArquivo(nomeArquivo):
    """
    Carrega um arquivo CSV utilizando separador ';' e codificação 'latin1'.
    """
    try:
        dados = pd.read_csv(nomeArquivo, sep=";", encoding="latin1")
        print("Arquivo carregado com sucesso!\n")
        print(f"Formato original: {dados.shape}\n")
        return dados
    except FileNotFoundError:
        print(f"Erro: o arquivo '{nomeArquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Não foi possível carregar o arquivo. Erro: {e}")
        return None


def executarTestesExploratorios(dados):
    """
    Executa testes exploratórios iniciais no dataset.
    """
    print("\n=== TESTE EXPLORATÓRIO DO DATASET ===\n")

    print("Informações das colunas:")
    print(dados.info())
    print()

    print("Primeiras 10 linhas:")
    print(dados.head(10))
    print()

    colunas_teste = [col for col in ["uf", "sexo", "mortos", "causa_acidente"] if col in dados.columns]
    dados_teste = dados[colunas_teste].copy()

    print("Colunas selecionadas para teste:")
    print(dados_teste.head(10))
    print()

    if "uf" in dados_teste.columns and "mortos" in dados_teste.columns:
        mortes_por_estado = dados_teste.groupby("uf")["mortos"].sum()
        print("Soma de mortes por estado:")
        print(mortes_por_estado)
        print()

        media_por_estado = dados_teste.groupby("uf")["mortos"].mean()
        print("Média de mortes por estado:")
        print(media_por_estado)
        print()

    if "sexo" in dados_teste.columns and "uf" in dados_teste.columns:
        dados_filtrados = dados_teste[dados_teste["sexo"] != "Não Informado"]
        sexo_por_estado = dados_filtrados.groupby(["uf", "sexo"]).size().unstack(fill_value=0)
        print("Quantidade por estado e sexo:")
        print(sexo_por_estado)
        print()


def tratamentoArquivo(dados):
    """
    Seleciona colunas úteis, remove valores inválidos e cria colunas auxiliares.
    """
    #print("Informações do arquivo original:")
    #print(dados.info())
    #print()

    col_uteis = ["uf", "sexo", "mortos", "causa_acidente", "data_inversa"]
    colunas_existentes = [col for col in col_uteis if col in dados.columns]
    dados_tratados = dados[colunas_existentes].copy()

    linhas_antes = dados_tratados.shape[0]

    if "sexo" in dados_tratados.columns:
        dados_tratados = dados_tratados[
            (dados_tratados["sexo"] != "Não Informado") &
            (dados_tratados["sexo"] != "Ignorado")
        ]

    if "data_inversa" in dados_tratados.columns:
        dados_tratados["data_inversa"] = pd.to_datetime(
            dados_tratados["data_inversa"], errors="coerce"
        )
        dados_tratados["mes"] = dados_tratados["data_inversa"].dt.month

    mapa_regiao = {
        "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte",
        "RO": "Norte", "RR": "Norte", "TO": "Norte",
        "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste",
        "MA": "Nordeste", "PB": "Nordeste", "PE": "Nordeste",
        "PI": "Nordeste", "RN": "Nordeste", "SE": "Nordeste",
        "DF": "Centro-Oeste", "GO": "Centro-Oeste",
        "MT": "Centro-Oeste", "MS": "Centro-Oeste",
        "ES": "Sudeste", "MG": "Sudeste",
        "RJ": "Sudeste", "SP": "Sudeste",
        "PR": "Sul", "RS": "Sul", "SC": "Sul"
    }

    if "uf" in dados_tratados.columns:
        dados_tratados["regiao"] = dados_tratados["uf"].map(mapa_regiao)

    dados_tratados.dropna(inplace=True)

    linhas_depois = dados_tratados.shape[0]
    removidas = linhas_antes - linhas_depois

    print("Tratamento concluído.")
    print(f"Linhas antes do tratamento: {linhas_antes}")
    print(f"Linhas removidas: {removidas}")
    print(f"Linhas restantes: {linhas_depois}\n")
    print("Amostra dos dados tratados:")
    print(dados_tratados.head(10))
    print()

    return dados_tratados


def separarTreinoTeste(dados, tamanho_teste=0.3, random_state=42):
    """
    Divide o dataset em treino e teste.
    Tenta usar stratify, mas faz fallback caso haja pouca variabilidade em 'mortos'.
    """
    print("Separando treino e teste...")

    Y = dados["mortos"]
    X = dados.drop(["mortos"], axis=1)

    try:
        x_train, x_test, y_train, y_test = train_test_split(
            X,
            Y,
            test_size=tamanho_teste,
            train_size=1 - tamanho_teste,
            shuffle=True,
            random_state=random_state,
            stratify=Y
        )
        print("Split realizado com stratify em 'mortos'.")
    except ValueError as e:
        print(f"Aviso: não foi possível usar stratify. Motivo: {e}")
        print("Realizando split sem stratify...")
        x_train, x_test, y_train, y_test = train_test_split(
            X,
            Y,
            test_size=tamanho_teste,
            train_size=1 - tamanho_teste,
            shuffle=True,
            random_state=random_state
        )

    print(f"Treino: X={x_train.shape}, Y={y_train.shape}")
    print(f"Teste: X={x_test.shape}, Y={y_test.shape}")

    return x_train, x_test, y_train, y_test


def salvarArquivo(dados, nomeArquivo):
    dados.to_csv(nomeArquivo, index=False, sep=";", encoding="latin1")
    print(f"Arquivo salvo em: {nomeArquivo}")


def graficoTreinoTeste(x_train, x_test, pasta_saida):
    print("Gerando gráfico de treino x teste...")

    tamanhos = pd.Series({
        "Treino": len(x_train),
        "Teste": len(x_test)
    })

    fig, ax = plt.subplots(figsize=(7, 5))
    tamanhos.plot(kind="bar", ax=ax, color=["#2ca02c", "#d62728"], edgecolor="black")

    ax.set_ylabel("Quantidade de linhas")
    ax.set_title("Distribuição dos dados: Treino x Teste")
    ax.set_xticklabels(tamanhos.index, rotation=0)

    for i, valor in enumerate(tamanhos.values):
        ax.text(i, valor + max(tamanhos.values) * 0.01, str(valor), ha="center")

    plt.tight_layout()

    caminho = Path(pasta_saida) / "grafico_treino_teste.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()

    print(f"Gráfico salvo em: {caminho}")
    return str(caminho)


def graficoDistribuicaoMortosTreinoTeste(y_train, y_test, pasta_saida):
    print("Gerando gráfico da distribuição de 'mortos' no treino e no teste...")

    distribuicao = pd.DataFrame({
        "Treino": y_train.value_counts().sort_index(),
        "Teste": y_test.value_counts().sort_index()
    }).fillna(0).astype(int)

    fig, ax = plt.subplots(figsize=(8, 5))
    distribuicao.plot(kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e"], edgecolor="black")

    ax.set_xlabel("Classe de 'mortos'")
    ax.set_ylabel("Quantidade de registros")
    ax.set_title("Distribuição de 'mortos' no Treino e no Teste")
    ax.set_xticklabels(distribuicao.index.astype(str), rotation=0)
    ax.legend(title="Conjunto")

    for container in ax.containers:
        ax.bar_label(container, padding=3)

    plt.tight_layout()

    caminho = Path(pasta_saida) / "grafico_distribuicao_mortos_treino_teste.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()

    print(f"Gráfico salvo em: {caminho}")
    return str(caminho)


def visualizarDados(dados, pasta_saida="saida_relatorio"):
    """
    Gera gráficos e salva as imagens em disco.
    """
    Path(pasta_saida).mkdir(exist_ok=True)

    saidas = {
        "grafico_sexo_estado": None,
        "grafico_top_10_causas": None,
        "grafico_boxplot": None,
        "top_10_causas": None,
        "max_por_regiao": None,
    }

    if "uf" in dados.columns and "sexo" in dados.columns:
        sexo_por_estado = dados.groupby(["uf", "sexo"]).size().unstack(fill_value=0)
        estados = sexo_por_estado.index

        masculino = sexo_por_estado.get("Masculino", pd.Series(0, index=estados))
        feminino = sexo_por_estado.get("Feminino", pd.Series(0, index=estados))

        fig, ax = plt.subplots(figsize=(12, 6))
        width = 0.4
        x = range(len(estados))

        ax.bar(x, masculino, width, label="Masculino", color="#1f77b4")
        ax.bar([i + width for i in x], feminino, width, label="Feminino", color="#ff7f0e")

        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(estados, rotation=45, ha="right")
        ax.set_ylabel("Quantidade de Envolvidos")
        ax.set_title("Envolvidos em Acidentes por Estado e Sexo")
        ax.legend()

        plt.tight_layout()
        caminho_grafico1 = Path(pasta_saida) / "grafico_sexo_por_estado.png"
        plt.savefig(caminho_grafico1, dpi=150, bbox_inches="tight")
        plt.show()
        plt.close()

        saidas["grafico_sexo_estado"] = str(caminho_grafico1)

    if "causa_acidente" in dados.columns:
        top_10_causas = dados["causa_acidente"].value_counts().head(10)
        saidas["top_10_causas"] = top_10_causas

        fig2, ax2 = plt.subplots(figsize=(12, 6))
        top_10_causas.sort_values().plot(
            kind="barh",
            ax=ax2,
            color="skyblue",
            edgecolor="black"
        )

        ax2.set_xlabel("Quantidade de Ocorrências")
        ax2.set_ylabel("Causa do Acidente")
        ax2.set_title("Top 10 Principais Causas de Acidentes (2025)")

        plt.tight_layout()
        caminho_grafico2 = Path(pasta_saida) / "grafico_top_10_causas.png"
        plt.savefig(caminho_grafico2, dpi=150, bbox_inches="tight")
        plt.show()
        plt.close()

        saidas["grafico_top_10_causas"] = str(caminho_grafico2)

    if "regiao" in dados.columns and "mes" in dados.columns:
        agrupado = dados.groupby(["regiao", "mes"]).size().reset_index(name="qtd")

        regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
        dados_boxplot = []
        labels = []

        for reg in regioes:
            valores = agrupado[agrupado["regiao"] == reg]["qtd"]
            if not valores.empty:
                dados_boxplot.append(valores)
                labels.append(reg)

        if dados_boxplot:
            fig3, ax3 = plt.subplots(figsize=(10, 6))

            box = ax3.boxplot(
                dados_boxplot,
                tick_labels=labels,
                patch_artist=True,
                showfliers=False
            )

            cores = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2"]

            for patch, cor in zip(box["boxes"], cores):
                patch.set_facecolor(cor)
                patch.set_alpha(0.6)

            ax3.set_title("Distribuição da Quantidade de Acidentes por Região ao Longo dos Meses")
            ax3.set_xlabel("Região")
            ax3.set_ylabel("Quantidade de Acidentes por Mês")
            ax3.grid(axis="y", linestyle="--", alpha=0.3)

            plt.tight_layout()
            caminho_boxplot = Path(pasta_saida) / "grafico_boxplot.png"
            plt.savefig(caminho_boxplot, dpi=150, bbox_inches="tight")
            plt.show()
            plt.close()

            saidas["grafico_boxplot"] = str(caminho_boxplot)

        max_por_regiao = agrupado.loc[
            agrupado.groupby("regiao")["qtd"].idxmax()
        ]
        saidas["max_por_regiao"] = max_por_regiao

    print("Visualizações geradas com sucesso.\n")
    return saidas


def gerarMarkdown(arquivo_md, arquivo_csv, dados_originais, dados_limpos, resultados):
    """
    Gera um relatório Markdown com documentação e resultados da execução.
    """
    top_10 = resultados.get("top_10_causas")
    grafico1 = resultados.get("grafico_sexo_estado")
    grafico2 = resultados.get("grafico_top_10_causas")
    grafico3 = resultados.get("grafico_boxplot")
    max_por_regiao = resultados.get("max_por_regiao")

    linhas_originais = dados_originais.shape[0]
    linhas_tratadas = dados_limpos.shape[0]
    colunas_originais = ", ".join(dados_originais.columns)
    colunas_tratadas = ", ".join(dados_limpos.columns)
    percentual_restante = (linhas_tratadas / linhas_originais * 100) if linhas_originais else 0

    markdown = f"""# Relatório de Análise de Acidentes de Trânsito - 2025

**Data de geração:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  
**Arquivo analisado:** `{arquivo_csv}`

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
- **Linhas originais:** {linhas_originais}
- **Linhas após tratamento:** {linhas_tratadas}
- **Linhas removidas:** {linhas_originais - linhas_tratadas}
- **Percentual mantido:** {percentual_restante:.2f}%

### 3.2 Colunas
- **Colunas originais:** {colunas_originais}
- **Colunas tratadas:** {colunas_tratadas}

---

## 4. Gráficos Gerados
"""

    if grafico1:
        markdown += f"\n### 4.1 Envolvidos por Estado e Sexo\n\n![Envolvidos por Estado e Sexo]({grafico1})\n"
    if grafico2:
        markdown += f"\n### 4.2 Top 10 Causas de Acidentes\n\n![Top 10 Causas de Acidentes]({grafico2})\n"
    if grafico3:
        markdown += f"\n### 4.3 Boxplot Região x Mês\n\n![Boxplot Região x Mês]({grafico3})\n"

    markdown += "\n---\n\n## 5. Top 10 Causas de Acidentes\n"

    if top_10 is not None and not top_10.empty:
        markdown += "\n| Causa do acidente | Quantidade |\n|---|---:|\n"
        for causa, quantidade in top_10.items():
            markdown += f"| {causa} | {quantidade} |\n"
    else:
        markdown += "\nNenhum dado disponível para o ranking de causas.\n"

    markdown += "\n---\n\n## 6. Mês com Mais Acidentes por Região\n"

    if max_por_regiao is not None and not max_por_regiao.empty:
        markdown += "\n| Região | Mês | Quantidade |\n|---|---:|---:|\n"
        for _, row in max_por_regiao.iterrows():
            markdown += f"| {row['regiao']} | {int(row['mes'])} | {int(row['qtd'])} |\n"
    else:
        markdown += "\nNenhum dado disponível para o resumo por região.\n"

    markdown += "\n---\n\n## 7. Conclusão\n\nO script foi executado com sucesso.\n"

    with open(arquivo_md, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Relatório Markdown gerado com sucesso em: {arquivo_md}")


if __name__ == "__main__":
    arquivo_csv = "projeto26.csv"
    arquivo_md = "relatorio_acidentes_2025.md"

    dados_originais = carregarArquivo(arquivo_csv)

    if dados_originais is not None:
        executarTestesExploratorios(dados_originais)
        dados_limpos = tratamentoArquivo(dados_originais)

        x_train, x_test, y_train, y_test = separarTreinoTeste(dados_limpos)

        Path("saida_relatorio").mkdir(exist_ok=True)
        salvarArquivo(dados_limpos, "dados_tratados.csv")

        grafico_treino = graficoTreinoTeste(x_train, x_test, "saida_relatorio")
        grafico_mortos = graficoDistribuicaoMortosTreinoTeste(y_train, y_test, "saida_relatorio")

        resultados = visualizarDados(dados_limpos)
        resultados["grafico_treino_teste"] = grafico_treino
        resultados["grafico_distribuicao_mortos_treino_teste"] = grafico_mortos

        gerarMarkdown(arquivo_md, arquivo_csv, dados_originais, dados_limpos, resultados)
    else:
        print("Falha ao carregar os dados. Encerrando execução.")