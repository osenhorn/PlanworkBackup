import sys
from telas import Janelas
from bancodedados import BancoDeDados
from configuracoes import ArqConf
from arquivos import GerenciaArquivos

if __name__ == '__main__':
    arquivo = GerenciaArquivos()
    if arquivo.existe():
        configarq = ArqConf()
        config = configarq.ler_config()
        banco = BancoDeDados(
            config['servidor'],
            config['usuario'],
            config['senha'],
            config['log'],
            config['prefixo'],
            config['pasta'])

        if len(sys.argv) > 1:
            if sys.argv[1] == 'auto':
                banco.executa()
        else:
            inicial = Janelas(
                config['servidor'],
                config['usuario'],
                config['senha'],
                config['log'],
                config['prefixo'],
                config['pasta'],
                config['cliente'],
                config['dias'])

            inicial.executa_telas()
    else:
        inicial = Janelas()
        inicial.executa_telas()
