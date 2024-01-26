from json_config import carrega_ou_cria_config

# valores padroes
visualizador_padroes = {
    'tamanho_fonte_inicial': 10,
    'qtd_linhas': 25,
    'qtd_colunas': 80,
    'cor_fonte_inicial': 'light gray',
    'cor_fundo': 'black',
    'fonte': 'Courier',
    'codepage': 'cp437',
    'exibe_scrollbar': True,
    'tela_cheia': False,
    'maximizado': False,
    'debug': False
}
# carrega valores do config e se não existir cria config com os valores padrões acima
visualizador_config = carrega_ou_cria_config('visualizador_config.json', visualizador_padroes)
