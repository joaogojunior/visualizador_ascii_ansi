from PIL import Image
from sys import argv, exit
from os import path
from pyinstaller_build_date import data_hora_build

versao = "0.1a"


def converter_imagem_para_ico(caminho_arquivo_entrada="icone.png", caminho_arquivo_ico="icone.ico", tamanho=256):
    # validando os inputs...
    # checa arquivo de entrada
    if not path.isfile(caminho_arquivo_entrada):
        print("Erro: Arquivo de entrada %s não existe!" % caminho_arquivo_entrada)
        exit(1)
    try:
        imagem = Image.open(caminho_arquivo_entrada)
        # converte para int se vier um str
        if isinstance(tamanho, str) and tamanho.isnumeric():
            tamanho = int(tamanho)
        elif isinstance(tamanho, int):
            pass
        else:
            print("Erro: tamanho (%s) deve ser um parâmetro numérico." % str(tamanho))
            exit(1)
        # checando se tamanho é um int válido
        if not 32 <= tamanho <= 256:
            print("Erro: Tamanho inválido, escolha um tamanho entre 32 e 256.")
            exit(1)
        print("Convertendo %s em %s (%sx%s)..." % (caminho_arquivo_entrada, caminho_arquivo_ico, tamanho, tamanho))
        # A biblioteca Pillow (PIL) suporta ícones multi-tamanho
        # Aqui, criamos um ícone de tamanho min 32 e maximo 256 pixels
        imagem = imagem.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
        # Salvar a imagem como ícone ICO
        imagem.save(caminho_arquivo_ico, format="ICO")
    except Exception as e:
        print("Erro: Não foi possível converter arquivo %s (%s)." % (caminho_arquivo_entrada, str(e)))
        exit(1)


def mostra_help(nome_script):
    nome_script = path.splitext(path.basename(nome_script))[0]
    print("Este app converte um arquivo de imagem suportado pela biblioteca Pillow para o formato .ico")
    print("Exemplo:")
    print("%s -h ou %s --help - esta mensagem." % (nome_script, nome_script))
    print("%s - cria icone.ico a partir de icone.png." % nome_script)
    print("%s entrada.png - cria icone.ico a partir de entrada.png." % nome_script)
    print("%s entrada.png saida.ico - cria saida.ico a partir de entrada.png." % nome_script)
    print("%s entrada.png saida.ico 32 - cria saida.ico a partir de entrada.png com tamanho 32x32." % nome_script)


if __name__ == "__main__":
    script, *argumentos = argv
    print("%s versão %s lançado em %s por João Guilherme <joaogojunior@gmail.com>" %
          (path.splitext(path.basename(script))[0], versao, data_hora_build))
    if "-h" in argumentos or "--help" in argumentos:
        mostra_help(script)
    elif len(argumentos) <= 3:
        converter_imagem_para_ico(*argumentos)
    else:
        print("Erro: no maximo 3 parâmetros podem ser definidos.")
        mostra_help(script)
