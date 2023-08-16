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
import shutil


def text_downloader(raw_text):
	b64 = base64.b64encode(raw_text.encode()).decode()
	new_filename = "NOTASAI.txt"
	st.markdown("#### Download arquivo NOTASAI.txt ###")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
	st.markdown(href,unsafe_allow_html=True)


def atualizarProdutos():
        
        st.title("Atualizar notasai.txt| Exportar txt!")

        form = st.form(key="integration")


        with form:
            cols = st.columns(2)
            #codigo = cols[0].text_input("Código Sage:")
            #cols = st.columns(2)
            #inicio_depreciacao = cols[0].date_input("Início da depreciação:")
            files = st.file_uploader("Selecionar arquivos", accept_multiple_files=True)
            submitted = st.form_submit_button(label="Submit")

        if submitted:
               if files is not None:
                    
                    #itens = []
                    #chaves = []
                    print(str(files[0].name).split('.'))
                    print(str(files[1].name).split('.'))
                    print(str(files[2].name).split('.'))
                    if str(files[0].name).split('.')[1] == 'xlsx':
                            file_produtos_sage = files[0]
                            if str(files[1].name).split('.')[0] == 'produtos_leste':
                                  file_produtos_leste = files[1]
                                  file_notasai = files[2]
                            else:
                                  file_produtos_leste = files[2]
                                  file_notasai = files[1]


                    df_produtos_leste = pd.read_csv(file_produtos_leste)
                    df_produtos_leste.insert(1,'chave_nota','')
                    print(df_produtos_leste.shape)
                    #print(df_produtos_leste.shape)
                    df_de_para = df_produtos_leste.copy()
                    for index, row in df_produtos_leste.iterrows():
                           df_de_para.iloc[index][0]= str(df_produtos_leste.iloc[index][0][49:59]) + '_' + str(unidecode.unidecode(df_produtos_leste.iloc[index][0][59:99]).rstrip(" "))
                           df_de_para.iloc[index][1] = str(df_produtos_leste.iloc[index][0][0:14]) + '_' + str(df_produtos_leste.iloc[index][0][36:42]) + '_' +str(unidecode.unidecode(df_produtos_leste.iloc[index][0][59:74]).rstrip(" ")) 
                    
                    #df_produtos_leste_final = df_produtos_leste.drop_duplicates(subset=['lesteFlu'])
                    
                    #Produtos_sage planilha
                    df_produtos_sage = pd.read_excel(file_produtos_sage, dtype = {'SEQ': str, 'CODLEST': str, 'CODSAGE': str})
                    #df_produtos_sage.columns.values[0] = "SEQ"
                    #df_produtos_sage['CODSAGE'] = df_produtos_sage['CODSAGE'].astype(str)
                    #planilha_produtos_sage = df_produtos_sage.copy()
                    df_produtos_sage.rename(columns = {'CHVLEST':'lesteFlu'}, inplace = True)
                    df_produtos_sage_final = df_produtos_sage.drop(['CODLEST', 'DESCRLEST', 'DESCRSAGE', 'EMPRESA'], axis=1)


                    df_merge = pd.merge(df_de_para,df_produtos_sage_final, how = 'left', on = 'lesteFlu')

                    #df_filtered = df_merge[df_merge['CODSAGE'].isna()]
                    #df_filtered_new = df_filtered.drop_duplicates(subset=['lesteFlu'])

                    #df_produtos_sage_novos = df_merge[df_merge['CODSAGE'].isna()]

                    #noData = '0'
                    #noDataSrt = ""
                    #tresData ='000'
                    #un = 'UN'
                    #sequencia = 0
                    '''
                    for index, row in df_filtered_new.iterrows():
                        lestFlu = str(row['lesteFlu'])
                        descricao = str(row['lesteFlu'].split('_')[1]).ljust(40)
                        #codigo = str(row['CODSAGE'])
                        codigo = str(int(codigo) + 1)

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
                    
                    #print(itens)
                    df_novos_itens = pd.DataFrame(chaves)
                    f = open('itens.txt','w', encoding="utf-8")
                    np.savetxt(f,itens, delimiter='',header='', fmt="%s")
                    #txt_file_itens = np.savetxt(f,itens, delimiter='',header='', fmt="%s")
                    f.close()

                    with open('itens.txt', 'r', encoding="utf-8") as arquivo:
                        todos_itens_novos = arquivo.read()
                    arquivo.close()
                    text_downloader(todos_itens_novos)
                    #print(final.shape)
                    #print(final)
                    final_novos_itens = df_novos_itens.rename(columns={df_novos_itens.columns[0]: 'lesteFlu', df_novos_itens.columns[1]: 'CODSAG'})
                    #print(su)
                    #final.columns.values[0] = "lesteFlu"
                    #final.columns.values[1] = "CODSAG"
                    #print(final)
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
                          
'''
                    file_notasai
                    df_notasai = pd.read_csv(file_notasai)
                    i = 1
                    df_notasai = pd.concat([df_notasai.iloc[:, :i],
                                            pd.DataFrame('', columns=['chave_nota','valor_icms','a_pis','a_cofins','base_pis','base_cofins','valor_pis','valor_cofins'], index=df_notasai.index),
                                            df_notasai.iloc[:, i:]], axis=1)
                    
                    df_notasai_de_para = df_notasai.copy()
                    #loop dataframe notasai
                    for index, row in df_notasai.iterrows():
                          num = index
                          if (num) <= len(df_notasai.index):
                                if df_notasai.iloc[num][0][0] == '1':
                                      cond = 1
                                      index_um = num
                                      while cond == 1:
                                            if df_notasai.iloc[num + 1][0][0] == '5':
                                                  num +=1
                                            elif df_notasai.iloc[num + 1][0][0] == '2':
                                                  df_notasai_de_para.iloc[num + 1][1] = df_notasai.iloc[index_um][0][50:68].replace('.', '').replace('/','').replace('-','').rstrip(" ").zfill(14)\
                                                                                + '_' + df_notasai.iloc[index_um][0][9:15] + '_' + str(unidecode.unidecode(df_notasai.iloc[num + 1][0][111:126])).rstrip(" ")
                                                  if str(df_notasai.iloc[num + 1][0][65:69]) != '0000':
                                                        valor = df_notasai.iloc[num + 1][0][57:69].lstrip('0')
                                                        pos = int(len(valor)-2)
                                                        valor_icms = round(float(valor[:pos] + "." + valor[pos:]) * 0.18,2)
                                                        a_pis = '0006500'
                                                        a_cofins = '0030000'
                                                        base_pis = df_notasai.iloc[num + 1][0][57:69]
                                                        base_cofins = df_notasai.iloc[num + 1][0][57:69]
                                                        valor_pis = round(float(valor[:pos] + "." + valor[pos:]) * 0.0065,2)
                                                        valor_cofins = round(float(valor[:pos] + "." + valor[pos:]) * 0.03,2)
                                                        df_notasai_de_para.iloc[num + 1][2] = str(valor_icms).replace('.','').zfill(12)
                                                        df_notasai_de_para.iloc[num + 1][3] = str(a_pis)
                                                        df_notasai_de_para.iloc[num + 1][4] = str(a_cofins)
                                                        df_notasai_de_para.iloc[num + 1][5] = str(base_pis)
                                                        df_notasai_de_para.iloc[num + 1][6] = str(base_cofins)
                                                        df_notasai_de_para.iloc[num + 1][7] = str(valor_pis).replace('.','').zfill(12)
                                                        df_notasai_de_para.iloc[num + 1][8] = str(valor_cofins).replace('.','').zfill(12)
                                                  else:
                                                        a_pis = '0016000'
                                                        a_cofins = '0076000'
                                                        df_notasai_de_para.iloc[num + 1][3] = str(a_pis)
                                                        df_notasai_de_para.iloc[num + 1][4] = str(a_cofins)
                                                  num +=1
                                                  if (num + 1) >= len(df_notasai.index):
                                                        cond = 2
                                            elif df_notasai.iloc[num + 1][0][0] == '1':
                                                  cond = 2

                    #print(df_notasai_de_para.shape)
                    df3 = df_merge.drop(['lesteFlu', 'SEQ'], axis=1)
                   # print(df3.head(5))
                    #print(df3.shape)
                    df_de_para_chave_nota = df3.drop_duplicates(subset=['chave_nota'])
                    #print(df_de_para_chave_nota.head(5))
                    #print(df_de_para_chave_nota.shape)
                    df_merge_final = pd.merge(df_notasai_de_para,df_de_para_chave_nota, how = 'left', on = 'chave_nota')
                    #print(df_merge_final.head(5))
                    #print(df_merge_final.shape)
                    inserir_txt_notasai_1 = [] 
                    inserir_txt_notasai_2 = []
                    #ns1 = open('notasai1.txt','w', encoding="utf-8")
                    for index, row in df_merge_final.iterrows():
                        if df_merge_final.iloc[index][0][0] == '2':
                              inserir = str(df_merge_final.iloc[index][0][:69]) + '01800' + str(df_merge_final.iloc[index][0][70:107]) + str(str(df_merge_final.iloc[index][9]).ljust(15)) + str(df_merge_final.iloc[index][0][126:143]) + str(str(df_merge_final.iloc[index][5]).zfill(12)) + str(df_merge_final.iloc[index][3])\
                                    + str(df_merge_final.iloc[index][0][162:189]) + str(str(df_merge_final.iloc[index][7]).zfill(12)) + str(df_merge_final.iloc[index][0][201:203]) + str(str(df_merge_final.iloc[index][6]).zfill(12))\
                                    + str(df_merge_final.iloc[index][4]) + str(df_merge_final.iloc[index][0][222:249]) + str(str(df_merge_final.iloc[index][8]).zfill(12)) + str(df_merge_final.iloc[index][0][261:278])\
                                    + str(str(df_merge_final.iloc[index][2]).zfill(12)) + str(df_merge_final.iloc[index][0][290:])
                        else:
                              inserir = df_merge_final.iloc[index]['lestFlu']
                        inserir_txt_notasai_1.append(inserir)
                        #ns1.write(inserir + '\n')

                    #with open('notasai1.txt', 'r') as f:
                          #st.download_button('Download Zip', f, file_name='NOTASAI.txt')
                          #if index <= 100000:
                        #inserir_txt_notasai_1.append(inserir)
                          #else:
                                #inserir_txt_notasai_2.append(inserir)
                    #df_merge_final_notasai = pd.DataFrame(inserir_txt_notasai_1)
                    #print(df_merge_final_notasai.shape)
                    #print(df_merge_final_notasai.head(5))
                    #save_path = 'H:\Drives compartilhados\Sage/'
                    #completeName = os.path.join(save_path,'notasai1.txt')  
                    ns1 = open('notasai.txt','w', encoding="utf-8")
                    np.savetxt(ns1,inserir_txt_notasai_1, delimiter='',header='', fmt="%s")

                    with open('notasai.txt', 'r') as notasai:
                        arquivo_notasai = notasai.read()
                    notasai.close()
                    text_downloader(arquivo_notasai)
                    #print(ns1)
                    #dest = 'H:\Drives compartilhados\TI\Sieg'
                    #try:
                        #shutil.copy(ns1, dest)
                    #except shutil.SameFileError:
                        #print("Source and destination represents the same file.")


'''
                    with open('notasai1.txt', 'r') as notasai1:
                        arquivo_notasai1 = notasai1.read()
                        #st.download_button('Download Zip', arquivo_notasai, file_name='NOTASAI.txt')
                        #arquivo_notasai = notasai.read()
                    #notasai.close()

                    
                    ns2 = open('notasai2.txt','w', encoding="utf-8")
                    np.savetxt(ns2,inserir_txt_notasai_2, delimiter='',header='', fmt="%s")

                    with open('notasai2.txt', 'r') as notasai2:
                        arquivo_notasai2 = notasai2.read()
                        #st.download_button('Download Zip', arquivo_notasai, file_name='NOTASAI.txt')
                        #arquivo_notasai = notasai.read()
                    #notasai.close()
                    text_downloader(arquivo_notasai1)
                    text_downloader(arquivo_notasai2)

                '''





