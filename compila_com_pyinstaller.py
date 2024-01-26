from datetime import datetime
from subprocess import run as subproc_run
from os import path

debug = False


def resource_path(relative_path):
    # checa se estamos rodando no ambiente do pyinstaller
    try:
        # esse import ira falhar fora do pyinstaller uma vez que o pyinstaller é quem cria a variavel _MEIPASS em sys
        from sys import _MEIPASS as MEIPASS
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = MEIPASS
        # concatena o valor em meipass com o nome de arquivo passado como parametro para obter o caminho absoluto do
        # arquivo dentro do diretorio temporario criado pelo pyinstaller
        retorno = path.join(base_path, path.basename(relative_path))
        if debug:
            print("found MEIPASS: %s " % retorno)
        return retorno
    except ImportError:
        # ja que nao estamos no pyinstaller apenas obtem o diretorio atual e concatena com o nome de arquivo na entrada
        # para obter o caminho absoluto do arquivo fornecido
        base_path = path.abspath(path.dirname(__file__))
        return path.join(base_path, path.basename(relative_path))


if __name__ == '__main__':
    # Caminho para o script principal
    scripts_compilar = ['visualizador.py', 'converte_img_em_ico.py']

    # Obtém a data e hora atual da compilação
    data_hora_compilacao = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    script_data_hora = 'pyinstaller_build_date.py'
    # Abre o arquivo emu_rom_launcher_build_date.py e adiciona a data/hora da compilação
    with open(script_data_hora, 'w') as arquivo_script:
        arquivo_script.write('data_hora_build = "%s"\n' % data_hora_compilacao)

    for script in scripts_compilar:
        # Comando PyInstaller para compilar o script principal
        icone = path.splitext(script)[0] + ".ico"
        subproc_run(['pyinstaller', '--icon=' + icone, '--add-data', icone + ';.',
                     '--upx-dir=D:\\apps win32 e AMD64\\compactadores\\upx-4.2.2-win64\\', '--onefile', script])
