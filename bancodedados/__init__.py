from arquivos import GerenciaArquivos
from datetime import datetime
import time
import pyodbc


class BancoDeDados:
    def __init__(self, servidor, usuario, senha, log, prefixo, pasta):
        self.arquivo = GerenciaArquivos()
        self.log = log
        self.prefixo = prefixo
        self.pasta = pasta
        self.driver = 'DRIVER={SQL Server};'
        self.dados_banco = '{0}SERVER={1};UID={2};PWD={3};'.format(self.driver, servidor,
                                                                   usuario, senha)
        self.bancos = []
        self.conexao = None
        self.cursor = None

    def conectar(self):
        try:
            self.conexao = pyodbc.connect(self.dados_banco, autocommit=True)
            return True

        except Exception as erro_conexao:
            dados_erro = f'Ocorreu um erro na conexão com o banco de dados. Erro:\n{erro_conexao}\n\n'
            with open(self.log, 'a') as log:
                log.write(f'{datetime.now()} - {dados_erro}')
            return False

    def listar_bancos(self):
        try:
            self.cursor = self.conexao.cursor()
            query_list = f"select name from sysdatabases where name like '{self.prefixo}%'"
            lista_bancos = self.cursor.execute(query_list)
            for banco in lista_bancos:
                self.bancos.append(banco[0])
            return True, self.bancos

        except Exception as erro_lista:
            dados_erro = f'Ocorreu um erro ao obter a lista dos bancos de dados. Erro:\n{erro_lista}\n\n'
            with open(self.log, 'a') as log:
                log.write(f'{datetime.now()} - {dados_erro}')
            return False, dados_erro

    def cria_backup(self, lista):
        try:
            for banco in lista:
                query_backup = f"backup database {banco} to disk= '{self.pasta}\\{banco}.bak'"
                self.cursor.execute(query_backup)
                mensagem_log = f'O arquivo {banco}.bak foi criado com sucesso.\n\n'
                with open(self.log, 'a') as log:
                    log.write(f'{datetime.now()} - {mensagem_log}')
                time.sleep(100 / 1000)
            return True

        except Exception as erro_backup:
            dados_erro = f'Ocorreu um erro ao fazer backup do banco de dados. Erro:\n{erro_backup}\n\n'
            with open(self.log, 'a') as log:
                log.write(f'{datetime.now()} - {dados_erro}')
            return False

    def executa(self):
        with open(self.log, 'a') as log:
            log.write(f'{datetime.now()} - Processo de backup iniciado.\n\n')
        conectou = self.conectar()
        if conectou:
            listou_banco = self.listar_bancos()
            if listou_banco[0]:
                criou_backup = self.cria_backup(listou_banco[1])
                if criou_backup:
                    if self.arquivo.executa(listou_banco[1]):
                        return True
                    else:
                        return False
