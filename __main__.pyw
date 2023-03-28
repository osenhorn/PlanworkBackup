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
        banco = BancoDeDados(config[0], config[1], config[2], config[3], config[4], config[5])
        if len(sys.argv) > 1:
            if sys.argv[1] == 'auto':
                banco.executa()
        else:
            inicial = Janelas(config[0], config[1], config[2], config[3], config[4], config[5], config[6])
            inicial.executa_telas()
    else:
        inicial = Janelas()
        inicial.executa_telas()
