from arquivos import GerenciaArquivos
from datetime import datetime
import pyodbc
import time
import os


class BancoDeDados:
    def __init__(self, servidor, usuario, senha, log, prefixo, pasta):
        self.log = f'{pasta}\\{log}'
        self.prefixo = prefixo
        self.pasta = pasta
        self.driver = 'DRIVER={SQL Server};'
        self.dados_banco = '{0}SERVER={1};UID={2};PWD={3};'.format(self.driver, servidor, usuario, senha)
        self.bancos = []
        self.conexao = None
        self.cursor = None

    def cria_backup(self):
        try:
            self.conexao = pyodbc.connect(self.dados_banco, autocommit=True)
        except Exception as erro_conexao:
            dados_erro = f'Ocorreu um erro na conexão com o banco de dados. Erro:\n{erro_conexao}\n\n'
            with open(self.log, 'a') as log:
                log.write(f'{datetime.now()} - {dados_erro}')
            return False

        try:
            self.cursor = self.conexao.cursor()
            query_list = f"select name from sysdatabases where name like '{self.prefixo}%'"
            lista_bancos = self.cursor.execute(query_list)
        except Exception as erro_lista:
            dados_erro = f'Ocorreu um erro ao obter a lista dos bancos de dados. Erro:\n{erro_lista}\n\n'
            with open(self.log, 'a') as log:
                log.write(f'{datetime.now()} - {dados_erro}')
            return False

        try:
            itens = []
            for banco in lista_bancos:
                itens.append(banco[0])
            for item in itens:
                query_backup = f"backup database {item} to disk= '{self.pasta}\\tmp\\{item}.bak'"
                self.cursor.execute(query_backup)
                with open(self.log, 'a') as log:
                    log.write(f'{datetime.now()} - O arquivo {item}.bak foi criado com sucesso.\n\n')
                time.sleep(100 / 1000)
            return True
        except Exception as erro_backup:

            with open(self.log, 'a') as log:
                log.write(f'{datetime.now()} - Ocorreu um erro ao fazer backup do banco de dados.'
                          f'Erro:\n{erro_backup}\n\n')
            return False

    def executa(self):
        arquivos = GerenciaArquivos()
        if not arquivos.existe(f"{self.pasta}\\tmp"):
            os.mkdir(f"{self.pasta}\\tmp")
        with open(self.log, 'a') as log:
            log.write(f'{datetime.now()} - Processo de backup iniciado.\n\n')
        if self.cria_backup():
            if arquivos.executa():
                return True
            else:
                return False
        else:
            return False
