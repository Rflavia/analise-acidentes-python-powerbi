import pandas as pd
import matplotlib.pyplot as plt

# carregar o arquivo
def carregarArquivo(nomeArquivo):
    try:
        # Tenta ler o arquivo CSV
        dados = pd.read_csv(nomeArquivo, sep=";", encoding="latin1")
        print("Arquivo carregado com sucesso!\n")

    except Exception as e:
        print(f"Não foi possível carregar o arquivo. Erro: {e}")
        dados = None

    return dados

# tratamento do arquivo
def tratamentoArquivo(dados):
   
    #informações de colunas, tipo....
    print(dados.info())

    # Selecionar as colunas de interesse
    col_uteis = ["uf", "sexo", "mortos", "causa_acidente"]
    
    # Dica de reaproveitamento: só seleciona a coluna se ela existir no dataset
    colunas_existentes = [col for col in col_uteis if col in dados.columns]
    dados_tratados = dados[colunas_existentes].copy()

    # Limpeza dos dados: Remover 'Não Informado' da coluna sexo
    if "sexo" in dados_tratados.columns:
        dados_tratados = dados_tratados[dados_tratados["sexo"] != 'Não Informado']

    # Removemos linhas nulas caso existam nas colunas filtradas
    dados_tratados.dropna(inplace=True)

    print(f"\nTratamento concluído. Linhas restantes: {dados_tratados.shape[0]}\n")
    print(dados_tratados.head(10))
    return dados_tratados

# Função para visualizar os dados
def visualizarDados(dados):

    # GRÁFICO 1: Homens e Mulheres por Estado
    if "uf" in dados.columns and "sexo" in dados.columns:
        # Agrupar por estado e sexo
        sexo_por_estado = dados.groupby(["uf", "sexo"]).size().unstack(fill_value=0)
        
        estados = sexo_por_estado.index
        # Usar .get para evitar erro caso não tenha a categoria em algum dataset
        masculino = sexo_por_estado.get('Masculino', pd.Series(0, index=estados))
        feminino = sexo_por_estado.get('Feminino', pd.Series(0, index=estados))
        
        fig, ax = plt.subplots(figsize=(12, 6))
        width = 0.4
        x = range(len(estados))
        
        ax.bar(x, masculino, width, label='Masculino', color='#1f77b4')
        ax.bar([i + width for i in x], feminino, width, label='Feminino', color='#ff7f0e')
        
        ax.set_xticks([i + width/2 for i in x])
        ax.set_xticklabels(estados, rotation=45)
        ax.set_ylabel('Quantidade de Envolvidos')
        ax.set_title('Envolvidos em Acidentes por Estado e Sexo')
        ax.legend()
        
        plt.tight_layout()
        plt.show()


    # GRÁFICO 2: Top 10 Causas de Acidentes
    if "causa_acidente" in dados.columns:
        top_10_causas = dados['causa_acidente'].value_counts().head(10)
        
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        # .sort_values() inverte para a barra maior ficar no topo
        top_10_causas.sort_values().plot(kind='barh', ax=ax2, color='skyblue', edgecolor='black')
        
        ax2.set_xlabel('Quantidade de Ocorrências')
        ax2.set_ylabel('Causa do Acidente')
        ax2.set_title('Top 10 Principais Causas de Acidentes (2025)')
        
        plt.tight_layout()
        plt.show()


# FLUXO PRINCIPAL DO PROGRAMA

# Carrega os dados
dados_originais = carregarArquivo('acidentes2025.csv')
if dados_originais is not None:
    # Trata os dados
    dados_limpos = tratamentoArquivo(dados_originais)
    # Gera os gráficos
    visualizarDados(dados_limpos)


 # SALVAR CSV LIMPO
    dados_limpos.to_csv('dados_tratados.csv', index=False)
    
    visualizarDados(dados_limpos) 