#importando bibliotecas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


#configurando terminal para mostrar mais informações
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.options.display.float_format = '{:.2f}'.format

#chamando tabela ja limpa, filtrando a ultima linha "total" para não interferir na nossas analises
df = pd.read_csv('DATABASE_LIMPO.csv')
df_analise = df[df['Região Metropolitana - RIDE'] != 'Total']


#Buscando infomações exenciais da tabela inteira
print("TAMANHO DA TABELA")
linhas = df_analise.shape[0]
colunas = df_analise.shape[1]
print(f"Temos {linhas} linhas (regiões, sem contar a linha total) e {colunas} colunas.\n")
print("-" * 60 + "\n")
print("\n")

print("INFORMAÇÕES TÉCNICAS DAS COLUNAS")
df_analise.info()
print("-" * 60 + "\n")
print("\n")

print("ESTATÍSTICA")
pd.options.display.float_format = '{:.2f}'.format 
print(df_analise.describe())
print("-" * 60 + "\n")
print("\n")

#função para extrarir informações individuais de todas as colunas
def analisar_colunas_individuais(tabela):
    array_de_colunas = []
    for nome_coluna in tabela.columns:
        if pd.api.types.is_numeric_dtype(tabela[nome_coluna]):
            array_de_colunas.append(nome_coluna)
            coluna_isolada = tabela[nome_coluna]
            
            contagem = coluna_isolada.count()
            media = coluna_isolada.mean()
            mediana = coluna_isolada.median()
            listaModa = coluna_isolada.mode()
            moda = listaModa[0] if len(listaModa) > 0 else 0

            minimo = coluna_isolada.min()
            primeiroQuartil = coluna_isolada.quantile(0.25)
            terceiroQuartil = coluna_isolada.quantile(0.75)
            maximo = coluna_isolada.max()

            
            desvioPadrao = coluna_isolada.std()
            variancia = coluna_isolada.var()
            amplitude = maximo - minimo
            iqr = terceiroQuartil - primeiroQuartil
            
            cv = (desvioPadrao / media) * 100 if media != 0 else 0

            print(f"Analise: {nome_coluna}")
            print(f"Analise feita em {contagem} regiões")
            print("TENDÊNCIA CENTRAL:")
            print(f"Média: {media:.2f}")
            print(f"Mediana: {mediana:.2f}")
            print(f"Moda: {moda:.2f}")
            print("-" * 40)
            print("MEDIDAS DE POSIÇÃO:")
            print(f"Mínimo: {minimo:.2f}")
            print(f"Primeiro Quartil: {primeiroQuartil:.2f}")
            print(f"Terceiro Quartil: {terceiroQuartil:.2f}")
            print(f"Maximo: {maximo:.2f}")
            print("-" * 40)
            print("MEDIDAS DE DISPERSÃO:")
            print(f"Amplitude Total: {amplitude:.2f}")
            print(f"Intervalo Interquartil (IQR): {iqr:.2f}")
            print(f"Variância: {variancia:.2f}")
            print(f"Desvio Padrão: {desvioPadrao:.2f}")
            print(f"  Coef. de Variação (CV): {cv:.2f}%")
            print("-" * 40)
            print("=" * 30 + "\n")
    
    return array_de_colunas


#chamando a função que nos da a analise individual de cada coluna
print("Análise estatística completa...\n")
minhas_colunas_salvas = analisar_colunas_individuais(df_analise)
print("Análise concluída!!")
print("-" * 60 + "\n")
print("\n")

#selecionando colunas numericas para dados de correlação
print("\nGerando Matriz de Correlação (Heatmap)...")
df_numerico = df_analise.select_dtypes(include=['number'])
apelidos = {
    'Rede geral - sem informação de canalização': 'Rede Geral',
    'Poço ou nascente - sem informação de canalização': 'Poço (Prop.)',
    'Poço ou nascente fora da propriedade': 'Poço (Fora)',
    'Carro-Pipa': 'Carro-Pipa',
    'Água da chuva armazenada em cisterna': 'Chuva (Cist.)',
    'Água da chuva armazenada outra forma': 'Chuva (Outra)',
    'Rio, açude, lago ou igarapé': 'Rio/Lagos',
    'Poço ou nascente na aldeia': 'Poço (Aldeia)',
    'Poço ou nascente fora da aldeia': 'Poço (F. Aldeia)',
    'Outra': 'Outras'
}
df_numerico_curto = df_numerico.rename(columns=apelidos)
matriz_corr = df_numerico_curto.corr()
#print(matriz_corr.to_string(float_format="{:.2f}".format))
#print("-" * 60 + "\n")
#como não consegui apresentar de forma clara no terminal, optei por criar um grafico


#criando mapa de calor
plt.figure(figsize=(12, 8))
sns.heatmap(matriz_corr, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Matriz de Correlação: Formas de Abastecimento de Água')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('correlacao.png')
plt.show()
print("-" * 60 + "\n")
print("\n")

#Buscando por valores perdidos ou incorretos!
valores_nulos = df_analise.isnull().sum()
colunas_com_nulos = valores_nulos[valores_nulos > 0]
if colunas_com_nulos.empty:
    print("Não existe valores faltantes na nossa base")
else:
    print("Valores em branco:")
    print(colunas_com_nulos)

df_numerico_auditoria = df_analise.select_dtypes(include=['number'])
valores_negativos = (df_numerico_auditoria < 0).sum()
colunas_com_negativos = valores_negativos[valores_negativos > 0]
if colunas_com_negativos.empty:
    print("Nenhum valor logicamente incorreto")
else:
    print("Valores negativos inconsistentes encontrados nas colunas:")
    print(colunas_com_negativos)
print("-" * 60 + "\n")
print("\n")


#função para localizar anomalias na nossa tabela
def relatorio_geral_outliers(tabela):
    df_numerico = tabela.select_dtypes(include=['number']).drop(columns=['Total'], errors='ignore')
    for nome_coluna in df_numerico.columns:
        Q1 = tabela[nome_coluna].quantile(0.25)
        Q3 = tabela[nome_coluna].quantile(0.75)
        IQR = Q3 - Q1
        limite_superior = Q3 + 1.5 * IQR 
        outliers = tabela[tabela[nome_coluna] > limite_superior]
        
        if not outliers.empty:
            print(f"\nColuna: {nome_coluna.upper()} contem anomalias")
            print(f"Linha de corte do Estado: Acima de {limite_superior:.2f}")
            
            for index, linha in outliers.iterrows():
                regiao = linha['Região Metropolitana - RIDE']
                valor = linha[nome_coluna]
                print(f"   -> {regiao}: {valor:.0f} domicílios")
    
    print("\n" + "="*60 + "\n")

relatorio_geral_outliers(df_analise)