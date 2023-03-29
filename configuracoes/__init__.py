from datetime import date, timedelta
from pathlib import Path
import configparser
import base64
import os


class ArqConf:
    def __init__(self):
        self.arq_conf = str(os.getcwd() + '\\config.ini')
        self.senha = ''

    def grava_config(self, cliente, servidor, usuario, senha, prefixo, pasta):
        self.senha = senha.encode('utf-8')
        self.senha = str(base64.b64encode(self.senha))
        self.senha = self.senha[2:len(self.senha) - 1]
        config = configparser.ConfigParser()
        config['geral'] = {
            'caminhobackup': Path(pasta),
            'cliente': cliente
        }

        config['banco'] = dict(servidor=servidor,
                               usuario=usuario,
                               senha=self.senha,
                               prefixo=prefixo)
        try:
            with open(self.arq_conf, 'w') as configfile:
                config.write(configfile)
            return True, ''
        except OSError as erro:
            dados_erro = 'SEM PERMISSÃO PARA SALVAR O ARQUIVO DE CONFIGURAÇÃO.\n\nAltere as permissões no diretório'\
                    f' de instalação ou execute a aplicação como administrador.\n\nDescritivo do erro:\n\n{erro}'
            return False, dados_erro

    def ler_config(self):
        config = configparser.ConfigParser()
        config.read(self.arq_conf)
        senha = str(base64.b64decode(config['banco']['senha']))
        senha = senha[2:len(senha) - 1]
        pasta = Path(config['geral']['caminhobackup'])
        cliente = config['geral']['cliente']
        dados = {
            'servidor': config['banco']['servidor'],
            'usuario': config['banco']['usuario'],
            'senha': senha,
            'prefixo': config['banco']['prefixo'],
            'pasta': Path(config['geral']['caminhobackup']),
            'cliente': config['geral']['cliente'],
            'backup': Path(f'{pasta}\\{cliente}_BancoDeDados_{date.today()}.7z'),
            'backupapagar': Path(f'{pasta}\\{cliente}_BancoDeDados_{date.today() - timedelta(days=2)}.7z'),
            'log': Path(f'{pasta}\\{cliente}_BancoDeDados_{date.today()}.log'),
            'logapagar': Path(f'{pasta}\\{cliente}_BancoDeDados_{date.today() - timedelta(days=2)}.log')
        }
        return dados
