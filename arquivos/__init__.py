from configuracoes import ArqConf
from datetime import datetime
import py7zr
import shutil
import os


class GerenciaArquivos:
    def __init__(self):
        self.arq_conf = rf'{str(os.getcwd())}\config.ini'
        self.log = None
        self.pasta = None
        self.backup = None
        self.bkpapagar = None
        self.logapagar = None
        self.dias = None

    def compacta(self):
        try:
            tmpdir = f'{self.pasta}\\tmp'
            lista = os.listdir(tmpdir)
            with py7zr.SevenZipFile(f'{self.pasta}\\{self.backup}', 'w') as z:
                for arq in lista:
                    os.chdir(tmpdir)
                    z.writeall(arq)
            return True
        except Exception as erro:
            dados_erro = f'Ocorreu uma falha na compactação dos arquivos:\n{erro}'\
                    '\nOs arquivos .bak não foram apagados.\n\n'
            self.grava_log(dados_erro)
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

    def apagar_arquivo(self):
        os.chdir(self.pasta)
        self.grava_log(f'O arquivo {self.backup} foi criado com sucesso.\n\n')
        try:
            if self.existe(f'{self.pasta}\\{self.bkpapagar}'):
                os.remove(f'{self.pasta}\\{self.bkpapagar}')
                self.grava_log(f'O arquivo {self.bkpapagar}.bak foi excluído.\n\n')
        except Exception as erro_apagar:
            self.grava_log(f'Erro ao apagar o arquivo {self.bkpapagar}\n{erro_apagar}')

        try:
            if self.existe(self.logapagar):
                os.remove(self.logapagar)
                self.grava_log(f'O arquivo {self.logapagar}.bak foi excluído.\n\n')
        except Exception as erro_apagar:
            self.grava_log(f'Erro ao apagar o arquivo {self.logapagar}\n{erro_apagar}')

        try:
            shutil.rmtree(f'{self.pasta}/tmp')
            self.grava_log('Diretório temporário foi excluído.\n\n')
            self.grava_log('Arquivos ".bak" excluídos.\n\n')
            self.grava_log('Processo de backup concluído com sucesso.\n\n')
            return True
        except Exception as erro_apagar:
            self.grava_log(f'Erro ao apagar algum dos arquivos.\n{erro_apagar}')
            return False

    def grava_log(self, mensagem):
        with open(self.log, 'a') as log:
            log.write(f'{datetime.now()} - {mensagem}')

    def executa(self):
        arqconf = ArqConf()
        config = arqconf.ler_config()
        self.log = config['log']
        self.pasta = config['pasta']
        self.backup = config['backup']
        self.bkpapagar = config['backupapagar']
        self.logapagar = config['logapagar']
        self.dias = int(config['dias'])

        if self.compacta():
            if self.apagar_arquivo():
                return True
        return False
