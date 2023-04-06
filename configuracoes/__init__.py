from datetime import date, timedelta
import configparser
import base64
import os


class ArqConf:
    def __init__(self):
        self.arq_conf = f'{str(os.getcwd())}\\config.ini'
        self.senha = None
        self.dias = None

    def grava_config(self, cliente, servidor, usuario, senha, prefixo, pasta, dias):
        self.senha = senha.encode('utf-8')
        self.senha = str(base64.b64encode(self.senha))
        self.senha = self.senha[2:len(self.senha) - 1]
        config = configparser.ConfigParser()
        config['geral'] = {
            'caminhobackup': rf'{pasta}',
            'cliente': cliente
        }

        config['banco'] = {
            'servidor': servidor,
            'usuario': usuario,
            'senha': self.senha,
            'prefixo': prefixo,
            'dias': str(dias)}
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
        cliente = config['geral']['cliente']
        self.dias = int(config['banco']['dias'])
        dados = {
            'servidor': config['banco']['servidor'],
            'usuario': config['banco']['usuario'],
            'senha': senha,
            'prefixo': config['banco']['prefixo'],
            'pasta': config['geral']['caminhobackup'],
            'cliente': config['geral']['cliente'],
            'backup': f'{cliente}_BancoDeDados_{date.today()}.7z',
            'backupapagar': f'{cliente}_BancoDeDados_{date.today() - timedelta(days=self.dias)}.7z',
            'log': f'{cliente}_BancoDeDados_{date.today()}.log',
            'logapagar': f'{cliente}_BancoDeDados_{date.today() - timedelta(days=self.dias)}.log',
            'dias': self.dias
        }
        return dados
