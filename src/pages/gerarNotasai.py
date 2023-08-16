import pandas as pd
import numpy as np
import streamlit as st
import unidecode
from datetime import date
import base64
from io import BytesIO
import xlsxwriter
from pyxlsb import open_workbook as open_xlsb
import os
import re


def text_downloader(raw_text):
	b64 = base64.b64encode(raw_text.encode()).decode()
	new_filename = "ITEM.txt"
	st.markdown("#### Download arquivo ITEM.txt ###")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
	st.markdown(href,unsafe_allow_html=True)


def gerarNotasai():
        
        st.title("Atualizar Produtos| Exportar txt!")

        form = st.form(key="integration")


        with form:
            cols = st.columns(2)
            codigo = cols[0].text_input("Código Sage:")
            #cols = st.columns(2)
            #inicio_depreciacao = cols[0].date_input("Início da depreciação:")
            files = st.file_uploader("Selecionar arquivos", accept_multiple_files=True)
            submitted = st.form_submit_button(label="Submit")

        if submitted:
               if files is not None:
                    
                    itens = []
                    chaves = []
                    #print(str(files[0].name).split('.'))
                    if str(files[0].name).split('.')[1] == 'xlsx':
                            file_produtos_sage = files[0]
                            file_produtos_leste = files[1]
                    else:
                            file_produtos_leste = files[0]
                            file_produtos_sage = files[1]


                    df_produtos_leste = pd.read_csv(file_produtos_leste)
                    print(df_produtos_leste.shape)
                    #print(df_produtos_leste.shape)
                    for index, row in df_produtos_leste.iterrows():
                           df_produtos_leste.iloc[index][0] = str(df_produtos_leste.iloc[index][0][49:59]) + '_' + str(unidecode.unidecode(df_produtos_leste.iloc[index][0][59:99]).rstrip(" "))

                    df_produtos_leste_final = df_produtos_leste.drop_duplicates(subset=['lesteFlu'])

                    df_produtos_sage = pd.read_excel(file_produtos_sage, dtype = {'CODLEST': str, 'CODSAGE': str})
                    df_produtos_sage.columns.values[0] = "SEQ"
                    planilha_produtos_sage = df_produtos_sage.copy()
                    df_produtos_sage['CODSAGE'] = df_produtos_sage['CODSAGE'].astype(str)
                    df_produtos_sage.rename(columns = {'CHVLEST':'lesteFlu'}, inplace = True)
                    df_produtos_sage_final = df_produtos_sage.drop(['CODLEST', 'DESCRLEST', 'DESCRSAGE', 'EMPRESA'], axis=1)


                    df_merge = pd.merge(df_produtos_leste_final,df_produtos_sage_final, how = 'left', on = 'lesteFlu')

                    df_produtos_sage_novos = df_merge[df_merge['CODSAGE'].isna()]

                    noData = '0'
                    noDataSrt = ""
                    tresData ='000'
                    un = 'UN'
                    sequencia = 0
                    for index, row in df_produtos_sage_novos.iterrows():
                        lestFlu = str(row['lesteFlu'])
                        descricao = str(row['lesteFlu'].split('_')[1]).ljust(40)
                        #codigo = str(row['CODSAGE'])
                        codigo = int(codigo) + 1

                        #campos da layout txt sage
                        codigo_sage = str(codigo).zfill(10)
                        ncm = noData.zfill(8)
                        unidade = un.ljust(4)
                        peso = noData.zfill(9)
                        identificacao = str(codigo).ljust(15)
                        tipo_produto = '00'
                        brancos = noDataSrt.ljust(12)
                        entrada_icms = tresData
                        entrada_ipi = tresData
                        saida_icms = tresData
                        saida_ipi = tresData
                        unidade_dois = noDataSrt.ljust(382)
                        sequencia = sequencia + 1
                        sequencia_sage = str(sequencia).zfill(6)

                        itens_save = (codigo_sage,descricao,ncm,unidade,peso,
                                        identificacao,tipo_produto,brancos,entrada_icms,entrada_ipi,
                                        saida_icms,saida_ipi,unidade_dois,sequencia_sage)
                        
                        itens.append(itens_save)

                        chaves_save = (lestFlu,codigo)
                        chaves.append(chaves_save)
                    
                    final = pd.DataFrame(chaves)
                    print(final)
                    final_novos_itens = final.rename(columns={final.columns[0]: 'lesteFlu', final.columns[1]: 'CODSAG'})
                    df_merge_new = pd.merge(df_merge,final_novos_itens, how = 'left', on = 'lesteFlu')
                    df_merge_new.CODSAGE.fillna(df_merge_new.CODSAG, inplace=True)
                    final_novos_itens.insert(0, 'SEQ', '')
                    final_novos_itens.insert(2, 'CODLEST', '')
                    final_novos_itens.insert(3, 'DESCRLEST', '')
                    final_novos_itens.insert(5, 'DESCRSAGE', '')
                    final_novos_itens.insert(6, 'EMPRESA', 'FLGR')

                    seq = len(planilha_produtos_sage.index)
                    for index, row in final_novos_itens.iterrows():
                          seq = str(int(seq) + 1)
                          planilha_produtos_sage.loc[len(planilha_produtos_sage.index)] = [str(seq), str(final_novos_itens.iloc[index][1]), str(final_novos_itens.iloc[index][1][:10]),
                                                                   str(final_novos_itens.iloc[index][1][11:]),str(final_novos_itens.iloc[index][4]),
                                                                   str(final_novos_itens.iloc[index][1][11:]),'FLGR']

                    f = open('itens.txt','w', encoding="utf-8")
                    txt_file = np.savetxt(f,itens, delimiter='',header='', fmt="%s")
                    f.close()
                    #txt_file = np.savetxt('bens.txt', ativos, delimiter='',header='', fmt="%s", encoding = 'iso-8859-1')
                    #result = os.getenv('non-existent-variable', f)
                    #print(result) 
                    with open('itens.txt', 'r', encoding="utf-8") as arquivo:
                        todos_bens = arquivo.read()
                    arquivo.close()

                    text_downloader(todos_bens)

                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        planilha_produtos_sage.to_excel(writer, index=False, sheet_name='Sheet1') 
                        writer.close()
                        processed_data = buffer.getvalue()
                        st.download_button(
                              label="Download Excel worksheets",
                              data=buffer,
                              file_name="produtos_sage_atualizados.xlsx",
                              mime="application/vnd.ms-excel"
                        )
                    
                                
                           

                





