import os
import sys
import time
import py7zr
import shutil
import pyodbc
import winreg
import base64
import ctypes
from datetime import datetime
from datetime import date
from PySimpleGUI import PySimpleGUI as Gui


class DataBase:
    def __init__(self, server, user, passwd, file, prefix, path, days):
        self.file = file
        self.log = f'{path}\\{file}.log'
        self.prefix = prefix
        self.path = path
        self.database_info = "DRIVER={SQL Server};" + f'SERVER={server};UID={user};PWD={passwd};'
        self.databases = []
        self.days = days

    def create_backup(self):
        try:
            connection = pyodbc.connect(self.database_info, autocommit=True)
        except Exception as connection_error:
            error_data = f'Ocorreu um erro na conexão com o banco de dados. Erro:\n{connection_error}'
            self.save_log(error_data)
            return False, error_data

        try:
            cursor = connection.cursor()
            query_list = f"select name from sysdatabases where name like '{self.prefix}%'"
            database_list = cursor.execute(query_list)
        except Exception as list_error:
            error_data = f'Ocorreu um erro ao obter a lista dos bancos de dados. Erro:\n{list_error}'
            self.save_log(error_data)
            return False, error_data

        try:
            itens = []
            for database in database_list:
                itens.append(database[0])

            if not len(itens) > 0:
                error_data = (f'Ocorreu um erro ao obter a lista dos bancos de dados.\n'
                              f'Nenhum banco com prefixo "{self.prefix}" encontrado.\n'
                              f'Verifique as configurações.')
                self.save_log(error_data)
                return False, error_data

            for item in itens:
                query_backup = f"backup database {item} to disk= '{self.path}\\tmp\\{item}.bak'"
                cursor.execute(query_backup)
                self.save_log(f'O arquivo {item}.bak foi criado com sucesso.')
                time.sleep(100 / 1000)
            return True, ''
        except Exception as backup_error:
            error_data = f'Ocorreu um erro ao fazer backup do banco de dados. Erro:\n{backup_error}'
            self.save_log(error_data)
            return False, error_data

    def save_log(self, message):
        if self.path:
            with open(self.log, 'a') as log:
                if not message == '':
                    log.write(f'{datetime.now()}\n{message}\n\n')

    def run(self):
        files = ManageFiles(self.path, self.file, self.days)
        if not files.exist(f"{self.path}\\tmp"):
            os.mkdir(f"{self.path}\\tmp")
        self.save_log('Processo de backup iniciado.')
        result = self.create_backup()
        if result[0]:
            result = files.run()
            if result[0]:
                return result
            else:
                files.erase_temp()
        else:
            files.erase_temp()
        return result


class Config:
    @staticmethod
    def save(customer, server, user, passwd, prefix, path, days):
        pwd = passwd.encode('utf-8')
        pwd = str(base64.b64encode(pwd))
        pwd = pwd[2:len(pwd) - 1]
        try:
            reg = winreg.HKEY_LOCAL_MACHINE
            software = winreg.OpenKeyEx(reg, r"SOFTWARE")
            pwb = winreg.CreateKey(software, r"PlanWorkBackup")
            winreg.SetValueEx(pwb, "server", 0, winreg.REG_SZ, server)
            winreg.SetValueEx(pwb, "user", 0, winreg.REG_SZ, user)
            winreg.SetValueEx(pwb, "passwd", 0, winreg.REG_SZ, pwd)
            winreg.SetValueEx(pwb, "prefix", 0, winreg.REG_SZ, prefix)
            winreg.SetValueEx(pwb, "path", 0, winreg.REG_SZ, path)
            winreg.SetValueEx(pwb, "days", 0, winreg.REG_SZ, days)
            winreg.SetValueEx(pwb, "customer", 0, winreg.REG_SZ, customer)

            if pwb:
                winreg.CloseKey(pwb)
            return True, ''
        except Exception as error:
            return False, f'Erro ao salvar as configurações. Descritivo do erro:\n\n {error}'

    @staticmethod
    def read():
        try:
            reg = winreg.HKEY_LOCAL_MACHINE
            pwb = winreg.OpenKeyEx(reg, r"SOFTWARE\PlanWorkBackup")
            pwd = winreg.QueryValueEx(pwb, 'passwd')[0]
            pwd = str(base64.b64decode(pwd))
            pwd = pwd[2:len(pwd) - 1]
            customer = winreg.QueryValueEx(pwb, 'customer')[0]
            data = {
                'customer': customer,
                'days': winreg.QueryValueEx(pwb, 'days')[0],
                'path': winreg.QueryValueEx(pwb, 'path')[0],
                'prefix': winreg.QueryValueEx(pwb, 'prefix')[0],
                'passwd': pwd,
                'server': winreg.QueryValueEx(pwb, 'server')[0],
                'user': winreg.QueryValueEx(pwb, 'user')[0],
                'file': f'{customer}_BancoDeDados_{date.today()}'
            }
            return data
        except Exception as error:
            return f'Erro ao ler as configurações. Descritivo do erro:\n\n {error}'


class ManageFiles:
    def __init__(self, path, file, days):
        self.path = path
        self.file = file
        self.days = days

    def compact(self):
        self.save_log(f'Compactação dos arquivos iniciada.')
        try:
            tmpdir = f'{self.path}\\tmp'
            fileslist = os.listdir(tmpdir)
            with py7zr.SevenZipFile(f'{self.path}\\{self.file}.7z', 'w') as z:
                for arq in fileslist:
                    os.chdir(tmpdir)
                    z.writeall(arq)
            self.save_log(f'Compactação concluída. O arquivo {self.file}.7z foi criado com sucesso.')
            return True, ''
        except Exception as error:
            error_data = f'Ocorreu uma falha na compactação dos files:\n{error}' \
                         '\nOs arquivos .bak não foram apagados.'
            self.save_log(error_data)
            return False, error_data

    @staticmethod
    def exist(file):
        if os.path.exists(file):
            return True
        else:
            return False

    def erase_temp(self):
        try:
            shutil.rmtree(f'{self.path}/tmp')
        except Exception as erase_error:
            self.save_log(f'Erro ao excluir arquivos temporários.\n{erase_error}')

    def erase_file(self):
        try:
            os.chdir(self.path)
            file_list = os.listdir(self.path)
            if len(file_list) >= int(self.days) * 2:
                oldest_file = min(file_list, key=os.path.getctime).split('.')[0]
                os.remove(os.path.abspath(f'{oldest_file}.7z'))
                os.remove(os.path.abspath(f'{oldest_file}.log'))
                self.save_log(f'Os arquivos {oldest_file}.7z e {oldest_file}.log foram excluídos.')
        except Exception as erase_error:
            self.save_log(f'Erro ao apagar arquivo.\n{erase_error}')

        try:
            shutil.rmtree(f'{self.path}/tmp')
            self.save_log('Diretório temporário foi excluído.')
            self.save_log('Arquivos ".bak" excluídos.')
            self.save_log('Processo de backup concluído com sucesso.')
            return True, ''
        except Exception as erase_error:
            self.save_log(f'Erro ao excluir arquivos temporários.\n{erase_error}')
            return False, erase_error

    def save_log(self, message):
        if self.path:
            with open(f'{self.path}\\{self.file}.log', 'a') as log:
                if not message == '':
                    log.write(f'{datetime.now()}\n{message}\n\n')

    def run(self):
        done = self.compact()
        if done[0]:
            done = self.erase_file()
        return done


class Screens:
    def __init__(
            self,
            server=None,
            user=None,
            passwd=None,
            backup=None,
            prefix=None,
            path=None,
            customer=None,
            days=None):

        self.server = server
        self.user = user
        self.passwd = passwd
        self.prefix = prefix
        self.path = path
        self.customer = customer
        self.log = f'{backup}.log'
        self.days = days
        self.theme = 'Default1'
        self.config = Config()
        self.files = ManageFiles(path, backup, days)
        self.filled = True

    def configuration(self):
        Gui.theme(self.theme)
        layout = [[
            Gui.Frame(
                'Banco de dados', [
                    [Gui.Text('Endereço do servidor (Ex: 127.0.0.1):')],
                    [Gui.Input(key='server', size=(36, 1))],
                    [Gui.Text('Usuário (Ex.: sa):')],
                    [Gui.Input(key='user', size=(36, 1))],
                    [Gui.Text('Senha:')],
                    [Gui.Input(key='passwd', password_char='*', size=(36, 1))],
                    [Gui.Text('Prefixo do banco de dados (Ex.: sfb_):')],
                    [Gui.Input(key='prefix', size=(36, 1))]],
                size=(275, 250))],
            [
                Gui.Frame(
                    'Complementares',
                    [[Gui.Text('Nome do Cliente (Ex.: ACME):')],
                     [Gui.Input(key='customer', size=(36, 1))],
                     [Gui.Text('Quantos backups manter (Nº de dias):')],
                     [Gui.Input(key='days', size=(36, 1))],
                     [Gui.Text('Pasta onde o backup será salvo:')],
                     [Gui.FolderBrowse(target='path', button_text='Procurar', key='-LOCATE-PATH-'),
                      Gui.Input(key='path', disabled=True, size=(26, 1))],
                     [Gui.Text('', size=(16, 1))]],
                    size=(275, 200))],
            [
                Gui.Button('Salvar', key='-SAVE-CONFIG-', size=(8, 1)),
                Gui.Push(),
                Gui.Button('Fechar', key='-CLOSE-CONFIG-', size=(8, 1))]]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icon.ico',
            finalize=True)

    def existent(self):
        Gui.theme(self.theme)
        layout = [
            [Gui.Text("As configurações já existem.", key='EXISTENT-TEXT')],
            [Gui.Text('O que deseja fazer agora?\n')],
            [Gui.Radio('Executar um backup', 'ACTIONS', default=False, key='-EXECBKP-')],
            [Gui.Radio('Refazer as configurações', 'ACTIONS', default=False, key='-REDO-')],
            [Gui.Radio('Apenas encerrar o programa', 'ACTIONS', default=False, key='-CLOSE-')],
            [Gui.Text('')],
            [Gui.Push(), Gui.Button('OK', key='-CHOOSE-', size=(8, 1)), Gui.Push()]
        ]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icon.ico',
            finalize=True)

    def alert(self):
        Gui.theme(self.theme)
        layout = [
            [Gui.Text("", key='-TEXT-ALERT-')],
            [Gui.Push(), Gui.Button('OK', key='-CLOSE-ALERT-', size=(8, 1)), Gui.Push()]
        ]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icon.ico',
            finalize=True)

    def start_progress(self):
        Gui.theme(self.theme)
        layout = [
            [Gui.Text('O processo foi iniciado.\n\nSerá exibida uma nova mensagem quando for concluído.',
                      key='-PROGRESS-ALERT-')],
            [Gui.Push(),
             Gui.Button('AGUARDE...',
                        key='-CLOSE-PROGRESS-ALERT-',
                        size=(12, 2),
                        disabled=True),
             Gui.Push()]
        ]

        return Gui.Window(
            'Planwork',
            layout=layout,
            icon=r'./icon.ico',
            finalize=True,
        )

    # noinspection PyBroadException
    def run(self):
        configure = existent = alert = None
        if self.server:
            existent = self.existent()
            existent['-CHOOSE-'].bind('<Return>', '_Enter')
        else:
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                configure = self.configuration()
                configure['-LOCATE-PATH-'].bind('<Return>', '_Enter')
                configure['-SAVE-CONFIG-'].bind('<Return>', '_Enter')
                configure['-CLOSE-CONFIG-'].bind('<Return>', '_Enter')
            else:
                alert = self.alert()
                alert['-TEXT-ALERT-'].update(
                    'É preciso ser Administrador para realizar as configurações iniciais.')

        while True:
            active_screen, detected_event, got_value = Gui.read_all_windows()
            if detected_event == Gui.WINDOW_CLOSED:
                existent.close()
                break
            if detected_event in ['-CHOOSE-', '-CHOOSE-_Enter']:
                if got_value['-CLOSE-']:
                    existent.close()
                    break
                elif got_value['-REDO-']:
                    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                        configure = self.configuration()
                        configure['-LOCATE-PATH-'].bind('<Return>', '_Enter')
                        configure['-SAVE-CONFIG-'].bind('<Return>', '_Enter')
                        configure['-CLOSE-CONFIG-'].bind('<Return>', '_Enter')
                        configure['server'].update(self.server)
                        configure['user'].update(self.user)
                        configure['passwd'].update(self.passwd)
                        configure['prefix'].update(self.prefix)
                        configure['customer'].update(self.customer)
                        configure['path'].update(self.path)
                        configure['days'].update(self.days)
                        existent.close()
                    else:
                        alert = self.alert()
                        alert['-TEXT-ALERT-'].update(
                            'É preciso ser Administrador para alterar as configurações.')
                elif got_value['-EXECBKP-']:
                    alert_start = self.start_progress()
                    existent.close()
                    config_data = self.config.read()
                    database = DataBase(config_data['server'],
                                        config_data['user'],
                                        config_data['passwd'],
                                        config_data['file'],
                                        config_data['prefix'],
                                        config_data['path'],
                                        config_data['days'])
                    db_run = database.run()
                    if db_run[0]:
                        alert_start.close()
                        alert = self.alert()
                        alert['-TEXT-ALERT-'].update(
                            'Seu backup foi realizado com sucesso!\n\nO programa será encerrado.\n')
                    else:
                        alert_start.close()
                        alert = self.alert()
                        alert['-TEXT-ALERT-'].update(db_run[1])

            if detected_event in [Gui.WINDOW_CLOSED, '-CLOSE-CONFIG-', '-CLOSE-CONFIG-_Enter']:
                break
            elif detected_event in ['-SAVE-CONFIG-', '-SAVE-CONFIG-_Enter']:

                for i in got_value:
                    if i != '-LOCATE-PATH-':
                        if got_value[i] == '':
                            self.filled = False
                            break
                if not self.filled:
                    alert = self.alert()
                    alert['-TEXT-ALERT-'].update('Todos os campos são obrigatórios!')
                else:
                    self.server = got_value['server']
                    self.user = got_value['user']
                    self.passwd = got_value['passwd']
                    self.prefix = got_value['prefix']
                    self.path = got_value['path']
                    self.customer = got_value['customer']
                    try:
                        self.days = int(got_value['days'])
                        recorded = self.config.save(
                            got_value['customer'],
                            got_value['server'],
                            got_value['user'],
                            got_value['passwd'],
                            got_value['prefix'],
                            got_value['path'],
                            got_value['days']
                        )
                        configure.close()
                        if recorded[0]:
                            existent = self.existent()
                            existent['-CHOOSE-'].bind('<Return>', '_Enter')
                            existent['EXISTENT-TEXT'].update('CONFIGURAÇÃO CONCLUÍDA.\n\n')
                        else:
                            alert = self.alert()
                            alert['-TEXT-ALERT-'].update(recorded[1])
                    except Exception:
                        alert = self.alert()
                        alert['-TEXT-ALERT-'].update(
                            'O campo\n\n "Quantos backups manter (Nº de dias):"\n\n'
                            'deve receber um valor numérico e inteiro!')

            elif detected_event == "-LOCATE-PATH-_Enter":
                configure['-LOCATE-PATH-'].ButtonCallBack()

            if detected_event == '-CLOSE-ALERT-' or detected_event == Gui.WINDOW_CLOSED:
                if not self.filled:
                    self.filled = True
                alert.close()


if __name__ == '__main__':
    config = Config().read()
    if not isinstance(config, str):
        banco = DataBase(
            config['server'],
            config['user'],
            config['passwd'],
            config['file'],
            config['prefix'],
            config['path'],
            config['days']
        )

        if len(sys.argv) > 1:
            if sys.argv[1] == 'auto':
                banco.run()
        else:
            initial = Screens(
                config['server'],
                config['user'],
                config['passwd'],
                config['file'],
                config['prefix'],
                config['path'],
                config['customer'],
                config['days'])
            initial.run()
    else:
        inicial = Screens()
        inicial.run()
