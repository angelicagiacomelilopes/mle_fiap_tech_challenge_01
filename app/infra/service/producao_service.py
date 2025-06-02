import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
import pandas as pd
import logging
import os
import csv
from requests.exceptions import RequestException

class ProducaoService:
    def __init__(self, csv_path='data/producao_backup.csv'):
        self.csv_path = csv_path
        #self.backup_data = self.load_backup_data()

    def dataframe_para_json(self, df, ano, produto, categoria):
        # ano = '1971'
        # produto = 'VINHO DE MESA'
        # categoria = 'Tinto'
        print(ano, produto,categoria)
        df = df[df['ano'] == str(ano)]
        df = df[df['produto_principal'] == produto]
        df = df[
            (df['produto'] == categoria) |
            ((df['produto_principal'] == produto) & (df['produto'] == categoria) | (df['produto_principal'] == produto) & (df['produto'] == produto))
        ]
        print("primeiro filtro")
        print(df.head())

        # Criar estrutura base do JSON
        resultado = {
            "data": {},
            "metadata": {
                "fonte": "http://vitibrasil.cnpuv.embrapa.br",
                "unidade_quantidade": "litros"
            }
        }
        
        # Agrupar por ano e produto_principal
        grouped = df.groupby(['ano', 'produto_principal'])
  
        for (ano, produto_principal), group in grouped:
            # Formatar o ano como string
            ano_str = str(ano)
             
            total_principal = 0
            # Preparar a lista de categorias
            categorias = []
            
            print('produto_quantidade', total_principal)
            # Para cada produto dentro do grupo
           
            for _, row in group.iterrows():
                
                # Se o produto for diferente do produto_principal, adicionar como categoria
                if row['produto'] != produto_principal:
                    categorias.append({
                        "categoria": row['produto'],
                        "quantidade_litros": "{:,}".format(row['quantidade']).replace(",", ".")
                    })
                else:
                    print(row['produto_quantidade'])    
                    total_principal = row['produto_quantidade']  
                 
            # Criar a entrada do produto principal
            entrada_produto = {
                "produto": [{
                    "Nome": produto_principal,
                    "Quantidade_total_litros": "{:,}".format(total_principal).replace(",", "."),
                    "categorias": categorias
                }]
            }
            
            # Adicionar ao resultado
            if ano_str not in resultado["data"]:
                resultado["data"][ano_str] = []
            
            resultado["data"][ano_str].append(entrada_produto)
        
        return resultado

    # def transformar_dados(self,csv_path):
    #     # Carregar os dados do CSV
    #     df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
        
    #     # Filtrar linha de cabeçalho se existir (onde 'id' == 'id')
    #     df = df[df['id'] != 'id']
        
    #     # Selecionar colunas de interesse
    #     colunas_base = ['id', 'control', 'produto']
    #     colunas_anos = [str(ano) for ano in range(1970, 2024)]
        
    #     # Derreter (melt) o DataFrame - transformar colunas de anos em linhas
    #     df_transformado = pd.melt(
    #         df,
    #         id_vars=colunas_base,
    #         value_vars=colunas_anos,
    #         var_name='ano',
    #         value_name='quantidade'
    #     )
        
    #     # Converter quantidade para numérico (removendo pontos como separadores de milhar)
    #     df_transformado['quantidade'] = (
    #         df_transformado['quantidade'].astype(str)
    #         .str.replace('.', '', regex=False)
    #         .astype(int)
    #     )
        
    #     # Ordenar os dados
    #     df_transformado = df_transformado.sort_values(by=['produto', 'ano'])
        
    #     return df_transformado
    
    # def load_backup_data(self, ano = None, produto = None, categoria = None ) -> Dict[int, Dict[str, Any]]:
    #     """Carrega dados de backup do CSV"""
    #     if not os.path.exists(self.csv_path):
    #         return {}
       
       
    #     # Inicializar a estrutura de dados
    #     result = {
    #         "data": {},
    #         "metadata": {
    #             "fonte": "http://vitibrasil.cnpuv.embrapa.br",
    #             "unidade_quantidade": "litros"
    #         }
    #     }
        
    #     with open(self.csv_path, mode='r', encoding='utf-8') as csv_file:
    #         # Usar o delimitador de ponto e vírgula
    #         csv_reader = csv.DictReader(csv_file, delimiter=';')
            
    #         for row in csv_reader:
    #             # Pular a linha de cabeçalho se necessário
    #             if row['id'] == 'id':
    #                 continue
                
    #             # Extrair o nome do produto
    #             produto_nome = row['produto']
                 
    #             # Processar cada ano de 1970 a 2023
    #             for year in range(1970, 2024):
    #                 year_str = str(year)
    #                 quantidade = row.get(year_str, '0')
                    
    #                 # Remover possíveis pontos nos números (formato 1.000.000)
    #                 quantidade = quantidade.replace('.', '')
                    
    #                 # Criar a estrutura para o ano se não existir
    #                 if year_str not in result['data']:
    #                     result['data'][year_str] = []
                    
    #                 # Verificar se já existe uma entrada para este produto no ano
    #                 produto_entry = None
    #                 for entry in result['data'][year_str]:
    #                     if entry['produto'][0]['Nome'] == produto_nome:
    #                         produto_entry = entry
    #                         break
                    
    #                 # Se não existir, criar uma nova
    #                 if not produto_entry:
    #                     produto_entry = {
    #                         "produto": [
    #                             {
    #                                 "Nome": produto_nome,
    #                                 "Quantidade_total_litros": "0",
    #                                 "categorias": []
    #                             }
    #                         ]
    #                     }
                         
    #                     result['data'][year_str].append(produto_entry)
                        
    #                     return result 

    def processar_dados(self,csv_path):
        # Carregar o CSV
        df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
        
        # Remover linha de cabeçalho se existir
        df = df[df['id'] != 'id']
        
        # Criar coluna 'produto_principal' conforme regra especificada
        df['produto_principal'] = df.apply(
            lambda row: 'VINHO DE MESA' if str(row['control']).startswith('vm_') else 
                        'VINHO FINO DE MESA (VINIFERA)' if str(row['control']).startswith('vv_') else  
                        'SUCO' if str(row['control']).startswith('su_') else 
                        'DERIVADOS' if str(row['control']).startswith('de_') else 
            row['produto'],
            axis=1
        )
        
 
        # Selecionar colunas de anos
        anos_colunas = [str(ano) for ano in range(1970, 2024)]
        
        # Transformar para formato longo (unpivot)
        df_long = pd.melt(
            df,
            id_vars=['id', 'control', 'produto', 'produto_principal'],
            value_vars=anos_colunas,
            var_name='ano',
            value_name='quantidade'
        )
        
        df_long['produto_quantidade'] = df_long.apply(
            lambda row: row['quantidade'] if str(row['control']).startswith('VINHO DE MESA') else 
                        row['quantidade'] if str(row['control']).startswith('VINHO FINO DE MESA (VINIFERA)') else
                        row['quantidade'] if str(row['control']).startswith('SUCO') else
                        row['quantidade'] if str(row['control']).startswith('DERIVADOS') else 
            '0',
            axis=1
        )

        # Converter quantidade para inteiro (removendo separadores de milhar)
        df_long['quantidade'] = df_long['quantidade'].astype(str).str.replace('.', '').astype(int)
    
        return df_long
    
    def get_data(self, ano: Optional[int] = None, produto: Optional[str] = None, 
                categoria: Optional[str] = None) -> Dict[str, Any]:
        """Obtém dados para um intervalo de anos"""
        all_dfs = [] 
        
        url_teste = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
        if self.check_url_health(url_teste):
            print("Carregou on line")
            try:
                if ano is not None:
                
                    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02"
                    
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                        
                    df = self.explore_html(response.text)
                    if df is not None:
                        df['Ano'] = ano
                        all_dfs.append(df)
 

                else:
                    for ano in range(1970, 2024):
                        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02"
                        
                        try:
                            response = requests.get(url, timeout=10)
                            response.raise_for_status()
                            
                            df = self.explore_html(response.text)
                            if df is not None:
                                df['Ano'] = ano
                                all_dfs.append(df)
                        except requests.RequestException as e:
                            logging.warning(f"Erro ao acessar {url}: {str(e)}")
                            continue

                if not all_dfs:
                    return {"error": "Nenhum dado encontrado para os anos solicitados"}, 404

                final_df = pd.concat(all_dfs, ignore_index=True)
                
                # Aplicando filtros
                if ano is not None:
                    final_df = final_df[final_df['Ano'] == ano]
                
                if produto is not None:
                    final_df = final_df[final_df['produto'] == produto]

                if categoria is not None:
                    final_df = final_df[final_df['categoria'] == categoria]

                return self.build_data(final_df)
            
            except Exception as e:
                logging.error(f"Erro inesperado: {str(e)}")
                return {"error": f"Erro interno: {str(e)}"}, 500
        else:
            print("Carregou backup")
            df = self.processar_dados(self.csv_path)
            print(df.head())
            return self.dataframe_para_json(df, ano, produto, categoria)

    def check_url_health(self, url: str) -> bool:
        """Verifica se a URL está respondendo adequadamente"""
        try:
            response = requests.head(url, timeout=10)
            print(response.status_code)
            return response.status_code == 200
        except RequestException as e:
            logging.warning(f"Falha na verificação da URL {url}: {str(e)}")
            return False
        
    def explore_html(self, html_content: str) -> Optional[pd.DataFrame]:
        """Extrai dados de tabela HTML"""
        try:
            data = []
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
                elif 'tb_subitem' in cell_classes:
                    subitem = cells[0].get_text(strip=True)
                    subitem_value = cells[1].get_text(strip=True) if len(cells) > 1 else None
                    
                    if current_item and current_item_value:
                        data.append({
                            'produto': current_item,
                            'produto_quantidade_litros': current_item_value,
                            'categoria': subitem,
                            'categoria_quantidade_litros': subitem_value
                        })

            if not data:
                logging.warning("Nenhum dado extraído da tabela")
                return None

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
            
            # Verificação de estrutura - colunas básicas
            required_columns = {'produto', 'categoria', 'Ano'}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                raise ValueError(f"Colunas básicas faltando: {missing}")
            
            # Construção da estrutura de retorno
            result = {}
            
            for ano, ano_group in df.groupby('Ano'):
                ano_data = []
                
                for produto, produto_group in ano_group.groupby('produto'):
                    produto_data = {
                        "Nome": produto,
                        "Quantidade_total_litros": produto_group['produto_quantidade_litros'].iloc[0] if 'produto_quantidade_litros' in produto_group.columns else "N/A",
                        "categorias": [
                            {
                                "categoria": row['categoria'],
                                "quantidade_litros": row.get('categoria_quantidade_litros', 'N/A')
                            }
                            for _, row in produto_group.iterrows()
                        ]
                    }
                    ano_data.append({"produto": [produto_data]})
                
                result[str(ano)] = ano_data

            return {
                "data": result,
                "metadata": {
                    "fonte": "http://vitibrasil.cnpuv.embrapa.br",
                    "unidade_quantidade": "litros"
                }
            }

        except Exception as e:
            logging.error(f"Erro ao construir dados: {str(e)}")
            return {"error": f"Erro ao processar dados: {str(e)}"}, 500