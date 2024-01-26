# resolve probelama na chamada a exit com pyinstaller
from sys import exit
from tkinter import Tk, Text, Scrollbar, BOTH, INSERT, LEFT, RIGHT, Y, END, filedialog
from compila_com_pyinstaller import resource_path
from visualizador_conf import visualizador_config
from visualizador_textos import textos_dict, versao
from pyinstaller_build_date import data_hora_build

app_icone = "visualizador.ico"

# variaveis globais
tamanho_fonte_atual = visualizador_config['tamanho_fonte_inicial']


def aumentar_fonte(_event):
    global tamanho_fonte_atual
    tamanho_fonte_atual += 1
    texto_widget.configure(font=(visualizador_config['fonte'], tamanho_fonte_atual))


def diminuir_fonte(_event):
    global tamanho_fonte_atual
    if tamanho_fonte_atual > 1:
        tamanho_fonte_atual -= 1
        texto_widget.configure(font=(visualizador_config['fonte'], tamanho_fonte_atual))


def on_any_key(event):
    key_sequence = f"<{event.keysym}>"
    print(textos_dict['msg_key_press'] + key_sequence)


def move_cursor_home(_event):
    # move o cursor para o inicio do arquivo para ajudar na navegacao por setas
    texto_widget.mark_set(INSERT, "1.0")
    # move a visualizacao para o inicio do arquivo
    texto_widget.yview_moveto(0.0)


def move_cursor_end(_event):
    # move o cursor para o fim do arquivo para ajudar na navegaçao por setas
    texto_widget.mark_set(INSERT, END)
    # move a visualização para o fim do arquivo
    texto_widget.yview_moveto(1.0)


def on_close():
    janela_root.destroy()
    exit(0)  # Encerra o programa


def cria_janela_texto():
    root = Tk()
    root.iconbitmap(default=resource_path(app_icone))
    root.title(textos_dict['window_title'] % (versao, data_hora_build))
    text_widget = Text(root, wrap='word', width=visualizador_config['qtd_colunas'],
                       height=visualizador_config['qtd_linhas'],
                       font=(visualizador_config['fonte'], tamanho_fonte_atual),
                       bg=visualizador_config['cor_fundo'], fg=visualizador_config['cor_fonte_inicial'])
    # exibe widget de texto
    text_widget.pack(side=LEFT, fill=BOTH, expand=True)
    # exibe scrollbar
    if visualizador_config['exibe_scrollbar']:
        # Adicionar barras de rolagem (Scrollbar)
        scrollbar_y = Scrollbar(root, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar_y.set)
        # Configurar a posição dos widgets na janela
        scrollbar_y.pack(side=RIGHT, fill=Y)
    if visualizador_config['tela_cheia']:
        root.attributes('-fullscreen', True)
    elif visualizador_config['maximizado']:
        root.state('zoomed')
    # Adiciona atalhos de teclado
    # aumentar e diminuir a fonte
    root.bind("<plus>", aumentar_fonte)  # Tecla de adição no keypad
    root.bind("<minus>", diminuir_fonte)  # Tecla de subtração no keypad
    # esc para sair
    root.bind('<Escape>', lambda x: exit(0))
    # espaco faz o mesmo que page down
    root.bind('<space>', lambda event: text_widget.event_generate("<Next>"))
    # home vai pro inicio do arquivo
    root.bind('<Home>', move_cursor_home)
    # end vai pro fim do arquivo
    root.bind('<End>', move_cursor_end)
    # seta para cima sobe uma linha
    root.bind('<Up>', lambda event: text_widget.yview_scroll(-1, "units"))
    # seta para baixo desce uma linha
    root.bind('<Down>', lambda event: text_widget.yview_scroll(1, "units"))
    # f para tela cheia
    root.bind('<f>',
              lambda event: root.attributes('-fullscreen', False) if root.attributes('-fullscreen') else
              root.attributes('-fullscreen', True))
    if visualizador_config['debug']:
        # mostra como seria para capturar a tecla digitada
        root.bind("<Key>", on_any_key)

    # Adicionamos um tratamento para o fechamento da janela principal
    root.protocol("WM_DELETE_WINDOW", on_close)

    return root, text_widget


# cria a janela do tkinter
janela_root, texto_widget = cria_janela_texto()


def escolher_arquivo():
    janela_root.withdraw()
    arquivo_escolhido = filedialog.askopenfilename()
    janela_root.deiconify()
    return arquivo_escolhido


def finaliza_carregamento_janela():
    # faz widget readonly
    texto_widget.config(state='disabled')
    # Garantir que o foco esteja no widget Text
    texto_widget.focus_set()
    # move o cursor para home
    move_cursor_home(None)
    # print("vai pro mainloop")
    janela_root.mainloop()
