from json import loads, dumps
from os import path


def escreve_json_padrao(arquivo, json_padrao):
    with (open(arquivo, "w") as config):
        # salva json
        config.write(json_padrao)


# carrega valores padroes, cria arquivo de configuração caso nao exista
def carrega_ou_cria_config(arquivo, valores_padroes):
    if isinstance(valores_padroes, dict):
        # trata como dicionario e format json
        retorno = valores_padroes
        json_padrao = dumps(valores_padroes, indent=3)
    else:
        # trata como json e formata json
        retorno = loads(valores_padroes)
        json_padrao = dumps(retorno, indent=3)

    # testa se o arquivo de configuração existe
    if not path.isfile(arquivo):
        # se nao existir cria um com os defaults
        print("Arquivo de configuração %s não encontrado, criando um com padrões..." % arquivo)
        escreve_json_padrao(arquivo, json_padrao)
        return retorno
    else:
        # carrega config do arquivo
        dict_arquivo = carrega_config(arquivo)
        # checa se o arquivo tem precedência
        if len(dict_arquivo) == len(retorno):
            # se tiveram quantidades de opcoes iguais o arquivo é retornado
            return dict_arquivo
        else:
            # se tiverem quantidades diferentes entao atualiza com padroes novos
            # faz backup
            with open(arquivo, "r") as entrada:
                # rescreve backup antigo se existir
                with open(arquivo + "_backup", "w") as saida:
                    saida.write(entrada.read())
            print("Configuração está sendo atualizada, a configuração antiga foi salva como %s." % arquivo + "_backup")
            escreve_json_padrao(arquivo, json_padrao)
            return retorno


def carrega_config(arquivo):
    # carrega o arquivo de configuracao
    print("Carregando configurações de", arquivo + "...")
    with open(arquivo, "r") as config:
        return loads(config.read().strip())
