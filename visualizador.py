from os import path
from tkinter import END
# resolve problema na chamada a exit com pyinstaller
from sys import argv, exit
from visualizador_conf import visualizador_config
from janela_tkinter import texto_widget, escolher_arquivo, finaliza_carregamento_janela
from visualizador_textos import textos_dict, versao
from pyinstaller_build_date import data_hora_build


cor_texto_atual = visualizador_config['cor_fonte_inicial']


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding=visualizador_config['codepage'], errors='ignore') as arquivo_handler:
        retorno = arquivo_handler.read()
    return retorno


def converter_cor_ansi(cor_ansi):
    mapeamento_cores = {
        '30': 'black',
        '31': 'red',
        '32': 'green',
        '33': 'yellow',
        '34': 'blue',
        '35': 'magenta',
        '36': 'cyan',
        '37': 'white',
    }
    return mapeamento_cores.get(cor_ansi, visualizador_config['cor_fonte_inicial'])


def exibir_texto_formatado(texto):
    global cor_texto_atual
    # posicao na string que marca o inicio do codigo ansi
    inicio_codigo_ansi = -1
    # buffer do texto sem os codigos ansi
    texto_buffer = ""
    for i, char in enumerate(texto):
        if visualizador_config['debug']:
            print(textos_dict['debug_cod_ansi'], inicio_codigo_ansi != -1)
            if char == '\033':
                print(textos_dict['debug_char'], i, ord(char), "ESC")
            else:
                print(textos_dict['debug_char'], i, ord(char), char)
        # checa se o caractere é o caractere de escape ansi (esc)
        if char == '\033':
            # imprime buffer e reseta ele
            texto_widget.insert(END, texto_buffer, cor_texto_atual)
            texto_buffer = ""
            # salva o inicio do codigo_ansi
            inicio_codigo_ansi = i
            if visualizador_config['debug']:
                print(textos_dict['debug_ansi_start'], inicio_codigo_ansi)
        # checa se ja estamos dentro de um codigo ansi
        elif inicio_codigo_ansi >= 0:
            # checa se encontramos o fim do codigo ansi
            if char == 'm':
                if visualizador_config['debug']:
                    print(textos_dict['debug_ansi_end'], i)
                codigo_ansi = texto[inicio_codigo_ansi + 2:i]
                cor_texto_atual = converter_cor_ansi(codigo_ansi)
                texto_widget.tag_configure(cor_texto_atual, foreground=cor_texto_atual)
                # marca fim do codigo ansi
                inicio_codigo_ansi = -1
            # checa se o caractere é valido em um codigo ansi e se nao for significa que nao estamos mais dentro
            # de um codigo ansi.
            elif not char.isdigit() and not char == "[":
                if visualizador_config['debug']:
                    print(textos_dict['debub_premature_end'], i)
                inicio_codigo_ansi = -1
        # o caractere nao faz parte de um codigo ansi
        else:
            if visualizador_config['debug']:
                print(textos_dict['debug_put_char'], char)
            # adiciona o caractere ao buffer
            texto_buffer += char

    # descarrega o buffer no widget de texto do tkinter
    if len(texto_buffer) > 0:
        texto_widget.insert(END, texto_buffer, cor_texto_atual)
        del texto_buffer


if __name__ == "__main__":
    conteudo = None
    # checa se ao menos um argumento foi passado
    if len(argv) > 1:
        # checa se começa com '-h'
        if argv[1][:2] == "-h":
            # se for mostra manual
            ansi_text = ('\033[33m ▄▄▄        ██████  ▄████▄   ██▓ ██▓\n'
                         '▒████▄    ▒██    ▒ ▒██▀ ▀█  ▓██▒▓██▒\n'
                         '▒██  ▀█▄  ░ ▓██▄   ▒▓█    ▄ ▒██▒▒██▒\n'
                         '░██▄▄▄▄██   ▒   ██▒▒▓▓▄ ▄██▒░██░░██░\n'
                         ' ▓█   ▓██▒▒██████▒▒▒ ▓███▀ ░░██░░██░\n'
                         ' ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░▓  ░▓  \n'
                         '  ▒   ▒▒ ░░ ░▒  ░ ░  ░  ▒    ▒ ░ ▒ ░\n'
                         '  ░   ▒   ░  ░  ░  ░         ▒ ░ ▒ ░\n'
                         '      ░  ░      ░  ░ ░       ░   ░  \n'
                         '                   ░                \n'
                         '\033[31m ▄▄▄       ███▄    █   ██████  ██▓  \n'
                         '▒████▄     ██ ▀█   █ ▒██    ▒ ▓██▒  \n'
                         '▒██  ▀█▄  ▓██  ▀█ ██▒░ ▓██▄   ▒██▒  \n'
                         '░██▄▄▄▄██ ▓██▒  ▐▌██▒  ▒   ██▒░██░  \n'
                         ' ▓█   ▓██▒▒██░   ▓██░▒██████▒▒░██░  \n'
                         ' ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░▓    \n'
                         '  ▒   ▒▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░ ▒ ░  \n'
                         '  ░   ▒      ░   ░ ░ ░  ░  ░   ▒ ░  \n'
                         '      ░  ░         ░       ░   ░    \n'
                         '\033[37m')
            conteudo = ansi_text + textos_dict['text_manual'] % (versao, data_hora_build)
        else:
            # checa se foi passado um arquivo valido na linha de comando
            if path.isfile(argv[1]):
                # se foi le o conteudo do arquivo
                conteudo = ler_arquivo(argv[1])
            else:
                # o arquivo nao existe
                print(textos_dict['err_file_not_exist'])
                exit(1)
    else:
        # ja que nenhum parametro foi passado tenta selecionar um arquivo com o filedialog
        arquivo = escolher_arquivo()
        # testa se algum arquivo foi escolhido
        if arquivo:
            # se foi le o conteudo
            conteudo = ler_arquivo(arquivo)
        else:
            # mas se nao foi exibe erro e sai
            print(textos_dict['err_no_file'])
            exit(1)

    # se algum conteudo foi carregado exibe ele
    if conteudo:
        exibir_texto_formatado(conteudo)
        finaliza_carregamento_janela()
    else:
        # nehum conteudo ou arquivo vazio
        if visualizador_config['debug']:
            print(textos_dict['err_file_empty'])
