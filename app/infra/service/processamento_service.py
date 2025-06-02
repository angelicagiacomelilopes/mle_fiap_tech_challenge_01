import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any
from datetime import datetime
import pandas as pd
import logging
import json 
from requests.exceptions import RequestException
from data.processamento_backup import json_str

class ProcessamentoService:
    def __init__(self):
        self.backup_data = self.load_backup_data()

    def load_backup_data(self):
        try:
            print("Passou aqui")
            dados = json.loads(json_str)
            return dados
        except FileNotFoundError:
            print("Arquivo não encontrado.")
        except json.JSONDecodeError:
            print("Erro na formatação do JSON.")
    
    def get_data(self, year: Optional[int] = None, tipo: Optional[str] = None, 
                 subtipo: Optional[int] = None, cultivar: Optional[int] = None) -> Dict[str, Any]:
        # url_teste = "http://127.0.0.1:5000/processamentoa"
        url_teste = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
        if self.check_url_health(url_teste):
            print("Carregou on line")
                
        
            """Obtém dados para um intervalo de anos"""
            all_dfs = []
            dict_tipo = {
                'Viníferas': '01',
                'Americanas e híbridas': '02', 
                'Uvas de mesa': '03',
                'Sem classificação': '04'
            }

            try:
                if year is not None:
                    # Processamento para um ano específico
                    if tipo is not None:
                        # Processamento para tipo específico
                        valor = dict_tipo.get(tipo)
                        if valor is None:
                            return {"error": "Tipo de uva inválido"}, 400
                        
                        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_{valor}" 

                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        
                        df = self.explore_html(response.text)
                        
                        if df is not None: 
                            df['Ano'] = year 
                            df['Tipo'] = tipo 
                            all_dfs.append(df) 
                        
                    else:
                        # Processamento para todos os tipos no ano especificado
                        for tipo_nome, tipo_cod in dict_tipo.items():
                            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_{tipo_cod}" 
                            
                            response = requests.get(url, timeout=10)
                            response.raise_for_status()
                            
                            df = self.explore_html(response.text)
                            
                            if df is not None: 
                                df['Ano'] = year 
                                df['Tipo'] = tipo_nome 
                                all_dfs.append(df) 
                else:
                    # Processamento para todos os anos (1970-2023)
                    for ano in range(1970, 2024):
                        for tipo_nome, tipo_cod in dict_tipo.items():
                            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_{tipo_cod}"
                            
                            try:
                                response = requests.get(url, timeout=10)
                                response.raise_for_status()
                                
                                df = self.explore_html(response.text)
                            
                                if df is not None:
                                    df['Ano'] = ano
                                    df['Tipo'] = tipo_nome
                                    all_dfs.append(df)
                                
                            except requests.RequestException as e:
                                logging.warning(f"Erro ao acessar {url}: {str(e)}")
                                continue

                if not all_dfs:
                    return {"error": "Nenhum dado encontrado para os parâmetros solicitados"}, 404

                final_df = pd.concat(all_dfs, ignore_index=True)
                
                # Aplicando filtros
                if year is not None:
                    final_df = final_df[final_df['Ano'] == year]
                
                if tipo is not None:
                    final_df = final_df[final_df['Tipo'] == tipo]

                if subtipo is not None:
                    final_df = final_df[final_df['subtipo'] == subtipo]
                
                if cultivar is not None:
                    final_df = final_df[final_df['cultivar'] == cultivar]

                return self.build_data(final_df)

            except Exception as e:
                logging.error(f"Erro inesperado: {str(e)}")
                return {"error": f"Erro interno: {str(e)}"}, 500
        else:
            print("Carregou backup")
            print(self.backup_data)
            return self.backup_data

    def explore_html(self, html_content: str) -> Optional[pd.DataFrame]:
        """Extrai dados de tabela HTML"""
        try:
            data = []
            data_tipo = []
            current_item = None
            current_item_value = None

            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', {'class': 'tb_base tb_dados'})
           
            if not table:
                logging.warning("Tabela não encontrada no HTML")
                return None 
            
            for row in table.find_all('tr'):
         
                cells = row.find_all(['th', 'td'])
              
                if not cells:
                    continue         
                
                cell_classes = cells[0].get('class', [])
                
                 
                if 'tb_item' in cell_classes:
                    current_item = cells[0].get_text(strip=True)
                    current_item_value = cells[1].get_text(strip=True) if len(cells) > 1 else None

                    data_tipo.append({
                        'tipo': current_item,
                        'subtipo_quantidade': current_item_value 
                    })
                elif 'tb_subitem' in cell_classes:
                    subitem = cells[0].get_text(strip=True)
                    subitem_value = cells[1].get_text(strip=True) if len(cells) > 1 else None
                    
                    if current_item and current_item_value:
                        data.append({
                            'subtipo': current_item,
                            'subtipo_quantidade': current_item_value,
                            'cultivar': subitem,
                            'cultivar_quantidade': subitem_value
                        })
                
                

            if not data and not data_tipo:
                logging.warning("Nenhum dado extraído da tabela")
                return None
            elif not data and data_tipo:
                df = pd.DataFrame(data_tipo)
                logging.info(f"DataFrame criado com {len(df)} registros")
                return df    
            elif data and data_tipo:
                df = pd.DataFrame(data)
                logging.info(f"DataFrame criado com {len(df)} registros")
                return df

        except Exception as e:
            logging.error(f"Erro ao processar HTML: {str(e)}")
            return None
        
    def build_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Converte DataFrame para estrutura JSON aninhada"""
        try:
            # Limpeza dos dados
            df = df.map(lambda x: x.strip('[]') if isinstance(x, str) else x)
       
            # Verificação de estrutura
            required_columns = {'subtipo', 'subtipo_quantidade', 'cultivar', 'cultivar_quantidade', 'Ano', 'Tipo'}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                raise ValueError(f"Colunas obrigatórias faltando: {missing}")
            
            # Construção da estrutura aninhada
            result = {}

            for ano, ano_group in df.groupby('Ano'):
                ano_data = {}
                
                for tipo, tipo_group in ano_group.groupby('Tipo'):
                    tipo_data = [] 
                    
                    tipo_quantidade = tipo_group['subtipo_quantidade'].iloc[0] if not tipo_group.empty else "-"     
                    grouped = tipo_group.groupby('subtipo')
                    if grouped.ngroups == 0:
                        print("Nenhum grupo encontrado - o agrupamento está vazio")
                        
                        subtipo_data = {
                            "Nome": "-",
                            "Quantidade_total": tipo_quantidade,
                            "cultivares": []
                        }
                        tipo_data.append(subtipo_data)  
                    else:
                            
                        for subtipo, subtipo_group in grouped:
                            
                            subtipo_data = {
                                "Nome": subtipo,
                                "Quantidade_total": subtipo_group['subtipo_quantidade'].iloc[0],
                                "cultivares": [
                                    {
                                        "cultivar": row['cultivar'],
                                        "quantidade": row['cultivar_quantidade']
                                    }
                                    for _, row in subtipo_group.iterrows()
                                ]
                            }
                            
                            tipo_data.append(subtipo_data)  
                    

                    ano_data[tipo] = tipo_data
                
                result[str(ano)] = ano_data
 

            return {
                "data": result,
                "metadata": {
                    "fonte": "http://vitibrasil.cnpuv.embrapa.br",
                    "unidade_quantidade": "kg ou litros conforme o produto"
                }
            }
        except Exception as e:
            logging.error(f"Erro ao construir dados: {str(e)}")
            return {"error": f"Erro ao processar dados: {str(e)}"}
        
    def check_url_health(self, url: str) -> bool:
        """Verifica se a URL está respondendo adequadamente"""
        try:
            response = requests.head(url, timeout=10)
            print(response.status_code)
            return response.status_code == 200
        except RequestException as e:
            logging.warning(f"Falha na verificação da URL {url}: {str(e)}")
            return False        
        
    # def processar_dados(self,csv_path):
    #     # Carregar o CSV
    #     df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
        
    #     # Remover linha de cabeçalho se existir
    #     df = df[df['id'] != 'id']

         
    #     # Criar coluna 'produto_principal' conforme regra especificada
    #     df['produto_principal'] = df.apply(
    #         lambda row: 'TINTAS' if str(row['control']).startswith('ti_') else 
    #                     'BRANCAS E ROSADAS' if str(row['control']).startswith('br_') else  
    #                     'BRANCAS' if str(row['control']).startswith('br_') else 
    #         row['cultivar'],
    #         axis=1
    #     )
    
    
    #     # Selecionar colunas de anos
    #     anos_colunas = [str(ano) for ano in range(1970, 2024)]
        
    #     # Transformar para formato longo (unpivot)
    #     df_long = pd.melt(
    #         df,
    #         id_vars=['id', 'control', 'cultivar','produto_principal'],
    #         value_vars=anos_colunas,
    #         var_name='ano',
    #         value_name='quantidade'
    #     )
        
    #     df_long['produto_quantidade'] = df_long.apply(
    #         lambda row: row['quantidade'] if str(row['control']).startswith('TINTA') else 
    #                     # row['quantidade'] if str(row['control']).startswith('VINHO FINO DE MESA (VINIFERA)') else
    #                     # row['quantidade'] if str(row['control']).startswith('SUCO DE UVAS') else
    #                     # row['quantidade'] if str(row['control']).startswith('OUTROS PRODUTOS COMERCIALIZADOS') else 
    #                     # row['quantidade'] if str(row['control']).startswith('DERIVADOS') else
    #                     # row['quantidade'] if str(row['control']).startswith('VINHO ESPECIAL') else
    #                     # row['quantidade'] if str(row['control']).startswith('DERIVADOS') else
    #                     # row['quantidade'] if str(row['control']).startswith('ESPUMANTES') else
    #         '0',
    #         axis=1
    #     )

    #     print(df_long.head())
    #     # # Converter quantidade para inteiro (removendo separadores de milhar)
    #     # df_long['quantidade'] = df_long['quantidade'].astype(str).str.replace('.', '').astype(int)
    
    #     return df_long

    # def dataframe_para_json(self, df: pd.DataFrame, ano: Optional[int], 
    #                     tipo: Optional[str], subtipo: Optional[str], 
    #                     cultivar: Optional[str]) -> Dict[str, Any]:
    #     """Converte DataFrame para JSON com estrutura específica seguindo o formato exemplo"""
    #     try:
    #         # Aplicar filtros
    #         if ano is not None:
    #             df = df[df['ano'] == str(ano)]
    #         if tipo is not None:
    #             df = df[df['produto_principal'] == tipo]
    #         if subtipo is not None:
    #             df = df[df['control'] == subtipo]
    #         if cultivar is not None:
    #             df = df[df['cultivar'] == cultivar]

    #         resultado = {
    #             "data": {},
    #             "metadata": {
    #                 "fonte": "http://vitibrasil.cnpuv.embrapa.br",
    #                 "unidade_quantidade": "litros"
    #             }
    #         }

    #         for (ano, produto_principal), group in df.groupby(['ano', 'produto_principal']):
    #             ano_str = str(ano)
                
    #             if ano_str not in resultado["data"]:
    #                 resultado["data"][ano_str] = {}
                
    #             # Obter quantidade total do produto principal
    #             total_principal = group[group['cultivar'] == produto_principal]
    #             quantidade_total = total_principal['quantidade'].sum() if not total_principal.empty else "0"
                
    #             # Formatar para manter como string (com separador de milhar se necessário)
    #             if isinstance(quantidade_total, (int, float)):
    #                 quantidade_total = f"{quantidade_total:,}".replace(",", ".")
                
    #             # Criar lista de cultivares
    #             cultivares = []
    #             for _, row in group[group['cultivar'] != produto_principal].iterrows():
    #                 quantidade = row['quantidade']
    #                 if isinstance(quantidade, (int, float)):
    #                     quantidade = f"{quantidade:,}".replace(",", ".")
                    
    #                 cultivares.append({
    #                     "cultivar": row['cultivar'],
    #                     "quantidade": quantidade if quantidade != "0" else "-"
    #                 })
                
    #             # Adicionar ao resultado
    #             if produto_principal not in resultado["data"][ano_str]:
    #                 resultado["data"][ano_str][produto_principal] = []
                
    #             resultado["data"][ano_str][produto_principal].append({
    #                 "Nome": produto_principal,
    #                 "Quantidade_total": quantidade_total,
    #                 "cultivares": cultivares
    #             })

    #         return resultado
            
    #     except Exception as e:
    #         self.logger.error(f"Erro ao converter DataFrame para JSON: {str(e)}")
    #         return {"error": f"Erro ao processar dados: {str(e)}"}