from configuracoes import ArqConf
from datetime import datetime
import py7zr
import os


class GerenciaArquivos:
    def __init__(self):
        self.arq_conf = str(os.getcwd() + '\\config.ini')
        self.apagar = None
        self.log = None

    @staticmethod
    def compacta(lista_arquivos, logarq, pasta, backup):
        primeiro = True
        try:
            for arq in lista_arquivos:
                if primeiro:
                    with py7zr.SevenZipFile(backup, 'w') as z:
                        z.writeall(f'{pasta}\\{arq}.bak')
                    primeiro = False
                else:
                    with py7zr.SevenZipFile(backup, 'a') as z:
                        z.writeall(f'{pasta}\\{arq}.bak')
            with open(logarq, 'a') as log:
                log.write(f'{datetime.now()} - O arquivo {backup} foi criado com sucesso.\n\n')
            return True
        except Exception as erro:
            dados_erro = f'Ocorreu uma falha na compactação dos arquivos:\n{erro}'\
                    '\nOs arquivos .bak não foram apagados.\n\n'
            with open(logarq, 'a') as log:
                log.write(f'{datetime.now()} - {dados_erro}')
            return False

    def existe(self, arquivo=None):
        if arquivo is None:
            if os.path.exists(self.arq_conf):
                return True
            else:
                return False
        else:
            if os.path.exists(arquivo):
                return True
            else:
                return False

    def apagar_arquivo(self, arquivos, logarq, pasta, backupapagar, logapagar):
        if self.existe(backupapagar):
            try:
                os.remove(backupapagar)
                with open(logarq, 'a') as log:
                    log.write(f'{datetime.now()} - O arquivo {backupapagar}.bak foi excluído.\n\n')
            except Exception as erro_apagar:
                dados_erro = f'Erro ao apagar o arquivo {os.remove(backupapagar)}.bak\n{erro_apagar}'
                with open(logarq, 'a') as log:
                    log.write(f'{datetime.now()} - {dados_erro}')

        if self.existe(logapagar):
            try:
                os.remove(logapagar)
                with open(logarq, 'a') as log:
                    log.write(f'{datetime.now()} - O arquivo {logapagar}.bak foi excluído.\n\n')
            except Exception as erro_apagar:
                dados_erro = f'Erro ao apagar o arquivo {logapagar}.bak\n{erro_apagar}'
                with open(logarq, 'a') as log:
                    log.write(f'{datetime.now()} - {dados_erro}')

        try:
            for apagar in arquivos:
                self.apagar = apagar
                os.remove(f'{pasta}\\{apagar}.bak')
                with open(logarq, 'a') as log:
                    log.write(f'{datetime.now()} - O arquivo {self.apagar}.bak foi excluído.\n\n')
            with open(logarq, 'a') as log:
                log.write(f'{datetime.now()} - Processo de backup concluído.\n\n')
            return True
        except Exception as erro_apagar:
            dados_erro = f'Erro ao apagar o arquivo {self.apagar}.bak\n{erro_apagar}'
            with open(logarq, 'a') as log:
                log.write(f'{datetime.now()} - {dados_erro}')
            return False

    def executa(self, lista):
        arqconf = ArqConf()
        config = arqconf.ler_config()
        if self.compacta(
                lista,
                config['log'],
                config['pasta'],
                config['backup']):

            if self.apagar_arquivo(
                    lista,
                    config['log'],
                    config['pasta'],
                    config['backupapagar'],
                    config['logapagar']):

                return True
        return False
