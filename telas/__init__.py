from PySimpleGUI import PySimpleGUI as Gui
from arquivos import GerenciaArquivos
from bancodedados import BancoDeDados
from configuracoes import ArqConf


class Janelas:
    def __init__(
            self,
            servidor=None,
            usuario=None,
            senha=None,
            log=None,
            prefixo=None,
            pasta=None,
            cliente=None):

        self.servidor = servidor
        self.usuario = usuario
        self.senha = senha
        self.prefixo = prefixo
        self.pasta = pasta
        self.cliente = cliente
        self.log = log
        self.tema = 'Default1'
        self.arqconf = ArqConf()
        self.arquivos = GerenciaArquivos()
        self.banco = None
        self.fez_backup = False
        self.preenchido = True

    def configuracao(self):
        Gui.theme(self.tema)
        layout = [[
            Gui.Frame(
                'Banco de dados', [
                    [Gui.Text('Endereço do servidor (Ex: 127.0.0.1):')],
                    [Gui.Input(key='servidor', size=(36, 1))],
                    [Gui.Text('Usuário (Ex.: sa):')],
                    [Gui.Input(key='usuario', size=(36, 1))],
                    [Gui.Text('Senha:')],
                    [Gui.Input(key='senha', password_char='*', size=(36, 1))],
                    [Gui.Text('Prefixo do banco de dados (Ex.: sfb_):')],
                    [Gui.Input(key='prefixo', size=(36, 1))]],
                size=(275, 250))],
            [
                Gui.Frame(
                    'Complementares',
                    [[Gui.Text('Nome do Cliente (Ex.: ACME):')],
                     [Gui.Input(key='cliente', size=(36, 1))],
                     [Gui.Text('Pasta onde o backup será salvo:')],
                     [Gui.FolderBrowse(target='pasta', button_text='Procurar'),
                      Gui.Input(key='pasta', size=(26, 1))],
                     [Gui.Text('', size=(16, 1))]],
                    size=(275, 150))],
            [
                Gui.Button('Salvar', key='-SALVAR-CONFIG-', size=(8, 1)),
                Gui.Push(),
                Gui.Button('Fechar', key='-FECHAR-CONFIG-', size=(8, 1))]]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icone.ico',
            finalize=True)

    def existente(self):
        Gui.theme(self.tema)
        layout = [
            [Gui.Text("", key='TEXTO-EXISTENTE')],
            [Gui.Text('O que deseja fazer agora?\n')],
            [Gui.Radio('Executar um backup', 'ACOES', default=False, key='-EXECBKP-')],
            [Gui.Radio('Refazer as configurações', 'ACOES', default=False, key='-REFAZER-')],
            [Gui.Radio('Apenas encerrar o programa', 'ACOES', default=False, key='-ENCERRAR-')],
            [Gui.Text('')],
            [Gui.Push(), Gui.Button('OK', key='-ESCOLHER-', size=(8, 1)), Gui.Push()]
        ]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icone.ico',
            finalize=True)

    def alerta(self):
        Gui.theme(self.tema)
        layout = [
            [Gui.Text("", key='-TEXTO-ALERTA-')],
            [Gui.Push(), Gui.Button('OK', key='-FECHA-ALERTA-', size=(8, 1)), Gui.Push()]
        ]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icone.ico',
            finalize=True)

    def sair(self):
        Gui.theme(self.tema)
        layout = [
            [Gui.Text('Tem certeza que deseja encerrar o programa?\n')],
            [Gui.Button('Sim, fechar', key='-ENCERRA-APP', size=(8, 1)),
             Gui.Push(),
             Gui.Button('Retornar', key='-ANTERIOR-', size=(8, 1))]
        ]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icone.ico',
            finalize=True)

    def executa_telas(self):
        configurar = existente = sair = alerta = None
        if self.arquivos.existe():
            existente = self.existente()
            existente.set_icon(r'./icone.ico')
            existente['TEXTO-EXISTENTE'].update('ARQUIVO DE CONFIGURAÇÃO JÁ EXISTE.\n')
        else:
            configurar = self.configuracao()

        while True:
            janela, evento, valor = Gui.read_all_windows()
            if janela == existente:
                if evento == Gui.WINDOW_CLOSED:
                    existente.close()
                    break
                if evento == '-ESCOLHER-':
                    if valor['-ENCERRAR-']:
                        existente.close()
                        break
                    elif valor['-REFAZER-']:
                        configurar = self.configuracao()
                        configurar['servidor'].update(self.servidor)
                        configurar['usuario'].update(self.usuario)
                        configurar['senha'].update(self.senha)
                        configurar['prefixo'].update(self.prefixo)
                        configurar['cliente'].update(self.cliente)
                        configurar['pasta'].update(self.pasta)
                        existente.close()
                    elif valor['-EXECBKP-']:
                        existente.close()
                        config = self.arqconf.ler_config()
                        self.banco = BancoDeDados(config['servidor'], config['usuario'], config['senha'], config['log'],
                                                  config['prefixo'], config['pasta'])
                        if self.banco.executa():
                            alerta = self.alerta()
                            alerta['-TEXTO-ALERTA-'].update(
                                'Seu backup foi realizado com sucesso!\n\nO programa será encerrado.\n')
                        else:
                            alerta = self.alerta()
                            alerta['-TEXTO-ALERTA-'].update('Erro na execução do backup. Verifique os logs.')
                            existente.close()

            if janela == configurar:
                if evento == Gui.WINDOW_CLOSED or evento == '-FECHAR-CONFIG-':
                    sair = self.sair()
                elif evento == '-SALVAR-CONFIG-':
                    campos = [valor['cliente'], valor['servidor'], valor['usuario'], valor['senha'], valor['prefixo']]
                    for campo in campos:
                        if campo == '':
                            print("teste")
                            self.preenchido = False
                            break

                    if not self.preenchido:
                        alerta = self.alerta()
                        alerta['-TEXTO-ALERTA-'].update('Todos os campos são obrigatórios!')
                    else:
                        self.servidor = valor['servidor']
                        self.usuario = valor['usuario']
                        self.senha = valor['senha']
                        self.prefixo = valor['prefixo']
                        self.pasta = valor['pasta']
                        self.cliente = valor['cliente']
                        gravou = self.arqconf.grava_config(
                            valor['cliente'],
                            valor['servidor'],
                            valor['usuario'],
                            valor['senha'],
                            valor['prefixo'],
                            valor['pasta']
                        )
                        if gravou[0]:
                            configurar.close()
                            existente = self.existente()
                            existente['TEXTO-EXISTENTE'].update('CONFIGURAÇÃO CONCLUÍDA.\n\n')
                        else:
                            alerta = self.alerta()
                            alerta['-TEXTO-ALERTA-'].update(gravou[1])
                            configurar.close()

            if janela == alerta:
                if evento == Gui.WINDOW_CLOSED:
                    break
                if evento == '-FECHA-ALERTA-':
                    if not self.preenchido:
                        alerta.close()
                        self.preenchido = True
                    else:
                        break

            if janela == sair:
                if evento == Gui.WINDOW_CLOSED or evento == '-ENCERRA-APP':
                    break
                elif evento == '-ANTERIOR-':
                    sair.close()
