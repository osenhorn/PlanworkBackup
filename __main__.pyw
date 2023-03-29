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
        servidor = config[0]
        usuario = config[1]
        senha = config[2]
        log = config[3]
        prefixo = config[4]
        pasta = config[5]
        cliente = config[6]
        banco = BancoDeDados(servidor, usuario, senha, log, prefixo, pasta)
        if len(sys.argv) > 1:
            if sys.argv[1] == 'auto':
                banco.executa()
        else:
            inicial = Janelas(servidor, usuario, senha, log, prefixo, pasta, cliente)
            inicial.executa_telas()
    else:
        inicial = Janelas()
        inicial.executa_telas()
