import csv
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import filedialog
import tracker
from heatmapteste import VolleyballCourt, matrixcores

court = VolleyballCourt()

def fechar():
    exit()

def abrirtracker():
    def processar_video(video_path):
        tracker.main(video_path)  # Passa o caminho do vídeo para a função tracker.main()

    video_path = filedialog.askopenfilename(
        filetypes=[("Arquivos de vídeo", "*.mp4;*.avi;*.mkv;*.mov")])
    if video_path:
        processar_video(video_path)

def abrirdados():
    def verificar_arquivo_csv_vazio(nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            # Verifica se o arquivo está vazio
            for linha in leitor_csv:
                return False
        return True
    def heatmaps_callback(val):
        def callback():
            heatmaps(val)
        return callback
    nome_do_arquivo_csv = "player_positions.csv"
    config_janela = ctk.CTkToplevel(app)
    config_janela.title("Dados")
    config_janela.geometry("700x400")
    config_janela.resizable(width=False, height=False)
    if verificar_arquivo_csv_vazio(nome_do_arquivo_csv):
        label_texto = ctk.CTkLabel(master=config_janela, text="Ainda não existe dados", font=("Arial", 14))
        label_texto.pack(pady=5)
    else:
        tabview = ctk.CTkTabview(config_janela, width=400, corner_radius=20, border_width=5, border_color="red",
                                segmented_button_selected_color="blue", segmented_button_unselected_hover_color="blue")
        tabview.pack()

        tab_equipe_a = tabview.add("Equipa A")
        tab_equipe_b = tabview.add("Equipa B")
        tab_heatmap = tabview.add("HeatMap")

        # Criando os botões na aba HeatMap
        botao1 = ctk.CTkButton(tab_heatmap, text="Geral", command=heatmaps_callback(0))
        botao1.pack()

        espaco = ctk.CTkFrame(tab_heatmap, height=10)  # Espaço entre os botões
        espaco.pack()

        botao2 = ctk.CTkButton(tab_heatmap, text="Equipa A", command=heatmaps_callback(1))
        botao2.pack()

        espaco = ctk.CTkFrame(tab_heatmap, height=10)  # Espaço entre os botões
        espaco.pack()

        botao3 = ctk.CTkButton(tab_heatmap, text="Equipa B",command=heatmaps_callback(2))
        botao3.pack()

        tabview.tab("Equipa A").grid_columnconfigure(0, weight=1)
        tabview.tab("Equipa B").grid_columnconfigure(0, weight=1)
        tabview.tab("HeatMap").grid_columnconfigure(0, weight=1)


def heatmaps(val):
    if val == 0:
        court.draw(matrixcores,save_path='heatmap.png')
        messagebox.showinfo("Sucesso", "Download do HeatMap foi concluido!")
    elif val == 1:
        court.draw(matrixcores, columns=range(3),save_path='heatmapa.png')
        messagebox.showinfo("Sucesso", "Download do HeatMap foi concluido!")
    elif val == 2:
        court.draw(matrixcores, columns=range(3,6),save_path='heatmapb.png')
        messagebox.showinfo("Sucesso", "Download do HeatMap foi concluido!")

def abrir_configuracoes():
    config_janela = ctk.CTkToplevel(app)
    config_janela.title("Configurações")
    config_janela.geometry("300x200")

    def alterar_texto():
        novo_texto = entrada_texto.get()
        label.config(text=novo_texto)

    def alterar_tamanho():
        largura = entrada_largura.get()
        altura = entrada_altura.get()
        app.geometry(f"{largura}x{altura}")

    # Adicionar entradas e botões para alterar o texto do rótulo
    label_texto = ctk.CTkLabel(master=config_janela, text="Novo texto do rótulo", font=("Arial", 14))
    label_texto.pack(pady=5)

    entrada_texto = ctk.CTkEntry(master=config_janela, placeholder_text="Digite o novo texto")
    entrada_texto.pack(pady=5)

    botao_texto = ctk.CTkButton(master=config_janela, text="Alterar texto", command=alterar_texto)
    botao_texto.pack(pady=10)

    # Adicionar entradas e botões para alterar o tamanho da janela
    label_tamanho = ctk.CTkLabel(master=config_janela, text="Novo tamanho da janela (LxA)", font=("Arial", 14))
    label_tamanho.pack(pady=5)

    entrada_largura = ctk.CTkEntry(master=config_janela, placeholder_text="Largura")
    entrada_largura.pack(pady=5)

    entrada_altura = ctk.CTkEntry(master=config_janela, placeholder_text="Altura")
    entrada_altura.pack(pady=5)

    botao_tamanho = ctk.CTkButton(master=config_janela, text="Alterar tamanho", command=alterar_tamanho)
    botao_tamanho.pack(pady=10)

# Inicializar a aplicação
app = ctk.CTk()

# Cor conforme o sistema
ctk.set_appearance_mode("system")

# Definir o título da janela
app.title("VolleyBall Tracking")

# Definir o tamanho da janela
app.geometry("400x300")
app.resizable(False, False)

# Adicionar um rótulo
label = ctk.CTkLabel(master=app, text="Menu", font=("Arial", 16))
label.pack(pady=20)

button_config = ctk.CTkButton(master=app, text="Iniciar tracking", command=abrirtracker)
button_config.pack(pady=10)
button_config = ctk.CTkButton(master=app, text="Dados", command=abrirdados)
button_config.pack(pady=10)
button_config = ctk.CTkButton(master=app, text="Abrir Configurações", command=abrir_configuracoes)
button_config.pack(pady=10)
button_config = ctk.CTkButton(master=app, text="Sair", command=fechar)
button_config.pack(pady=10)

app.mainloop()
