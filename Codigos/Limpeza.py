import numpy as np
import pandas as pd


df = pd.read_csv('dados\DATABASE.csv', sep=';', encoding='latin1', skiprows=3, skipfooter=2, engine='python')
df.replace('-', 0, inplace=True)


colunas_numericas = df.columns[1:]
df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric)


df.to_csv('dados\DATABASE_LIMPO.csv', sep=',', encoding='utf-8-sig', index=False)


# 1. Carregamos a nossa base já limpa
df = pd.read_csv('DATABASE_LIMPO.csv')


#corrigindo nomes com erro
df.rename(columns={
    df.columns[0]: 'Região Metropolitana - RIDE', 
    df.columns[1]: 'Rede geral - sem informação de canalização',
    df.columns[2]: 'Poço ou nascente - sem informação de canalização',
    df.columns[3]: 'Poço ou nascente fora da propriedade',
    df.columns[4]: 'Carro-Pipa',
    df.columns[5]: 'Água da chuva armazenada em cisterna',
    df.columns[6]: 'Água da chuva armazenada outra forma',
    df.columns[7]: 'Rio, açude, lago ou igarapé',
    df.columns[8]: 'Poço ou nascente na aldeia',
    df.columns[9]: 'Poço ou nascente fora da aldeia',
    df.columns[10]: 'Outra'
}, inplace=True)

correcoes_regioes = {
    '35010 Sï¿½o Paulo - SP': 'São Paulo',
    '35020 Baixada Santista - SP': 'Baixada Santista',
    '35030 Campinas - SP': 'Campinas',
    '35041 V.Paraï¿½ba/Lit Nort 1 -SP': 'Vale do Paraíba 1',
    '35042 V.Paraï¿½ba/Lit Nort 2 -SP': 'Vale do Paraíba 2',
    '35043 V.Paraï¿½ba/Lit Nort 3 -SP': 'Vale do Paraíba 3',
    '35044 V.Paraï¿½ba/Lit Nort 4 -SP': 'Vale do Paraíba 4',
    '35045 V.Paraï¿½ba/Lit Nort 5 -SP': 'Vale do Paraíba 5',
    '35050 Jundiaï¿½ - SP': 'Jundiaí',
    '35060 Piracicaba - SP': 'Piracicaba',
    '35070 Sorocaba - SP': 'Sorocaba',
    '35900 Fora de Reg.Metrop. - SP': 'Interior (Fora RM)',
    '35000 Ignorado - SP': 'Não Informado'
}

df['Região Metropolitana - RIDE'] = df['Região Metropolitana - RIDE'].replace(correcoes_regioes)
df = df[df['Região Metropolitana - RIDE'] != 'Não Informado']

#salvando no arquivo
df.to_csv('DATABASE_LIMPO.csv', index=False)
