from json_config import carrega_ou_cria_config


# versao
versao = "0.1a"

# textos padrões
textos_padroes = {
    'debug_cod_ansi': "dentro de um codigo ansi:",
    'debug_char': "caractere:",
    'debug_ansi_start': "-> inicio codigo ansi:",
    'debug_ansi_end': "-> fim do codigo ansi:",
    'debug_premature_end': "-> fim prematuro do codigo ansi?",
    'debug_put_char': "-> coloca caractere no buffer...",
    'text_manual': ('Manual do visualizador de arquivos ASCII/ANSI %s lançado em %s\n'
                    'por João Guilherme de Oliveira Jr. <joaogojunior@gmail.com>\n'
                    '\n'
                    'Instruções:\n'
                    'Use as setas para cima e para baixo para subir ou descer uma linha.\n'
                    'Use as teclas PgUp e PgDown para avancar ou retroceder uma tela.\n'
                    'A tecla de espaco também avança para a próxima tela.\n'
                    'Use as teclas + e - para aumentar e diminuir a fonte do texto.\n'
                    'Aperte "f" para alternar entre tela cheia modo janela.\n'
                    'Para sair do visualizador tecle Esc.\n'
                    ),
    'err_file_not_exist': "Erro: O arquivo especificado não existe.",
    'err_no_file': "Erro: Nenhum arquivo selecionado.",
    'err_file_empty': 'Arquivo especificado está vazio.',
    'msg_key_press': "Tecla pressionada: ",
    'window_title': "Visualizador ASCII/ANSI v%s (%s) por João Guilherme <joaogojunior@gmail.com> - ESC p/ sair"
}
# carrega textos do arquivo e se não existir cria config com os valores padrões acima
textos_dict = carrega_ou_cria_config('default_txt.json', textos_padroes)
