import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
import pandas as pd
import logging
from requests.exceptions import RequestException
import json
from data.exportacao_backup import json_str
class ExportacaoService:
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
                pais: Optional[str] = None) -> Dict[str, Any]:
        
        # url_teste = "http://127.0.0.1:5000/processamentoa"
        url_teste = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
        if self.check_url_health(url_teste):
            print("Carregou on line")

            """Obtém dados de importação para um intervalo de anos"""
            all_dfs = []
            dict_tipo = {
                'Vinhos de mesa': '01',
                'Espumantes': '02', 
                'Uvas frescas': '03',
                'Suco de uva': '04'
            }

            try:
                if year is not None:
                    # Processamento para um ano específico
                    if tipo is not None:
                        # Processamento para tipo específico
                        valor = dict_tipo.get(tipo)
                        if valor is None:
                            return {"error": "Tipo de produto inválido"}, 400
                    
                        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_{valor}"
                        df = self._fetch_data(url, year, tipo)
                        if df is not None:
                            all_dfs.append(df)
                    else:
                        # Processamento para todos os tipos no ano especificado
                        for tipo_nome, tipo_cod in dict_tipo.items(): 
                            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_{tipo_cod}"
                            df = self._fetch_data(url, year, tipo_nome)
                            if df is not None:
                                all_dfs.append(df)
                else:
                    # Processamento para todos os anos (1970-2023)
                    for ano in range(1970, 2024):
                        for tipo_nome, tipo_cod in dict_tipo.items(): 
                            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_{tipo_cod}"
                            try:
                                df = self._fetch_data(url, ano, tipo_nome)
                                if df is not None:
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

                if pais is not None:
                    final_df = final_df[final_df['Pais'] == pais]

                return self.build_data(final_df)

            except Exception as e:
                logging.error(f"Erro inesperado: {str(e)}")
                return {"error": f"Erro interno: {str(e)}"}, 500
        else:
            print("Carregou backup")
            print(self.backup_data)
            return self.backup_data
                
    def check_url_health(self, url: str) -> bool:
        """Verifica se a URL está respondendo adequadamente"""
        try:
            response = requests.head(url, timeout=10)
            print(response.status_code)
            return response.status_code == 200
        except RequestException as e:
            logging.warning(f"Falha na verificação da URL {url}: {str(e)}")
            return False        
    

    def _fetch_data(self, url: str, year: int, tipo: str) -> Optional[pd.DataFrame]:
        """Busca dados da URL e retorna DataFrame"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            df = self.explore_html(response.text)
            
            if df is not None: 
                df['Ano'] = year 
                df['Tipo'] = tipo
                return df
            return None
        except requests.RequestException as e:
            logging.warning(f"Erro ao acessar {url}: {str(e)}")
            return None

    def explore_html(self, html_content: str) -> Optional[pd.DataFrame]:
        """Extrai dados de tabela HTML de importação"""
        try:
            data = []
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', {'class': 'tb_base tb_dados'})
           
            if not table:
                logging.warning("Tabela não encontrada no HTML")
                return None 
            
            # Extrai cabeçalhos da tabela
            headers = []
            header_row = table.find('tr', {'class': 'tb_header'})
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            
            # Extrai linhas de dados
            for row in table.find_all('tr'):
                if 'tb_header' in row.get('class', []):
                    continue  # Pula linha de cabeçalho
                
                cells = row.find_all(['th', 'td'])
                if not cells or len(cells) < 2:
                    continue
                
                # Para tabelas de importação, a estrutura é diferente
                row_data = {
                    'Pais': cells[0].get_text(strip=True),
                    'Quantidade': cells[1].get_text(strip=True),
                    'Valor': cells[2].get_text(strip=True) if len(cells) > 2 else None
                }
                data.append(row_data)

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
        """Converte DataFrame para estrutura JSON aninhada para importação"""
        try:
            # Limpeza dos dados
            df = df.map(lambda x: x.strip('[]') if isinstance(x, str) else x)
            
            # Verificação de colunas mínimas necessárias
            required_columns = {'Pais', 'Quantidade', 'Ano', 'Tipo'}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                raise ValueError(f"Colunas obrigatórias faltando: {missing}")
            
            # Construção da estrutura de retorno
            result = {}
            
            for ano, ano_group in df.groupby('Ano'):
                ano_data = {}
                
                for tipo, tipo_group in ano_group.groupby('Tipo'):
                    # Estrutura para armazenar dados por país
                    paises_data = {}
                    
                    for _, row in tipo_group.iterrows():
                        pais = row['Pais']
                        paises_data[pais] = {
                            "quantidade": row['Quantidade'],
                            "valor": row.get('Valor', 'N/A')   
                        }
                    
                    ano_data[tipo] = {
                        "total_paises": len(paises_data),
                        "paises": paises_data
                    }
                
                result[str(ano)] = ano_data

            return {
                "data": result,
                "metadata": {
                    "fonte": "http://vitibrasil.cnpuv.embrapa.br",
                    "unidade_quantidade": "kg ou litros conforme o produto",
                    "unidade_valor": "US$"
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