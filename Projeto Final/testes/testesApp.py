import tkinter as tk
from tkinter import ttk

def mostrar_velocidade_bola():
    # Aqui você colocaria o código para obter a velocidade da bola
    # Por enquanto, vamos apenas imprimir uma mensagem
    print("Velocidade da bola: XX m/s")  # Substitua XX pela velocidade real da bola

root = tk.Tk()
tabview = ttk.Notebook(root)

# Criando a primeira aba
tab_velocidades = ttk.Frame(tabview)
tabview.add(tab_velocidades, text="Velocidades")

# Criando o botão para mostrar a velocidade da bola na primeira aba
botao_mostrar_velocidade = tk.Button(tab_velocidades, text="Mostrar Velocidade", command=mostrar_velocidade_bola)
botao_mostrar_velocidade.pack()

# Criando a segunda aba
tab_outra_aba = ttk.Frame(tabview)
tabview.add(tab_outra_aba, text="Outra aba")

# Coloque aqui os widgets que você deseja adicionar à segunda aba
# Por exemplo:
# label_outra_aba = tk.Label(tab_outra_aba, text="Conteúdo da outra aba")
# label_outra_aba.pack()

# Exibindo o Notebook
tabview.pack()

root.mainloop()
