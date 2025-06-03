import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
import pandas as pd
import logging
from requests.exceptions import RequestException

class ComercializacaoService:
    def __init__(self, csv_path='data/comercio_backup.csv'):
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
    
    def processar_dados(self,csv_path):
        # Carregar o CSV
        df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
        
        # Remover linha de cabeçalho se existir
        df = df[df['id'] != 'id']
        
        # Criar coluna 'produto_principal' conforme regra especificada
        df['produto_principal'] = df.apply(
            lambda row: 'VINHO DE MESA' if str(row['control']).startswith('vm_') else 
                        'VINHO FINO DE MESA (VINIFERA)' if str(row['control']).startswith('vmf') else  
                        'OUTROS PRODUTOS COMERCIALIZADOS' if str(row['control']).startswith('ou_') else 
                        'DERIVADOS' if str(row['control']).startswith('de_') else 
                        'VINHO ESPECIAL' if str(row['control']).startswith('ve_') else 
                        'ESPUMANTES' if str(row['control']).startswith('es_') else 
                        'SUCO DE UVAS' if str(row['control']).startswith('su_') else 
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
                        row['quantidade'] if str(row['control']).startswith('SUCO DE UVAS') else
                        row['quantidade'] if str(row['control']).startswith('OUTROS PRODUTOS COMERCIALIZADOS') else 
                        row['quantidade'] if str(row['control']).startswith('DERIVADOS') else
                        row['quantidade'] if str(row['control']).startswith('VINHO ESPECIAL') else
                        row['quantidade'] if str(row['control']).startswith('DERIVADOS') else
                        row['quantidade'] if str(row['control']).startswith('ESPUMANTES') else
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
        # url_teste = "http://127.0.0.1:5000/producaoa"
        if self.check_url_health(url_teste):
            try:
                if ano is not None:
                    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04"
                    
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                        
                    df = self.explore_html(response.text)
                    if df is not None:
                        df['Ano'] = ano
                        all_dfs.append(df)
                else:
                    for ano in range(1970, 2024):
                        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04"
                        
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
                            'produto_quantidade': current_item_value,
                            'categoria': subitem,
                            'categoria_quantidade': subitem_value
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
            df = df.applymap(lambda x: x.strip('[]') if isinstance(x, str) else x)
            
            # Verificação de estrutura - colunas agora opcionais
            expected_columns = {'produto', 'categoria', 'Ano'}
            if not expected_columns.issubset(df.columns):
                missing = expected_columns - set(df.columns)
                raise ValueError(f"Colunas básicas faltando: {missing}")
            
            # Construção da estrutura de retorno
            result = {}
            
            for ano, ano_group in df.groupby('Ano'):
                ano_data = {}
                
                for produto, produto_group in ano_group.groupby('produto'):
                    produto_data = []
                    
                    for categoria, categoria_group in produto_group.groupby('categoria'):
                        item = {
                            "Nome": categoria,
                            "Quantidade_total_litros": categoria_group['produto_quantidade'].iloc[0] if 'produto_quantidade' in categoria_group.columns else "N/A",
                            "categorias": [
                                {
                                    "categoria": row['categoria'],
                                    "quantidade_litros": row['categoria_quantidade'] if 'categoria_quantidade' in row else "N/A"
                                }
                                for _, row in categoria_group.iterrows()
                            ]
                        }
                        produto_data.append(item)
                    
                    ano_data[produto] = produto_data
                
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
        
    def check_url_health(self, url: str) -> bool:
        """Verifica se a URL está respondendo adequadamente"""
        try:
            response = requests.head(url, timeout=10)
            print(response.status_code)
            return response.status_code == 200
        except RequestException as e:
            logging.warning(f"Falha na verificação da URL {url}: {str(e)}")
            return False