import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('player_positions.csv', header=None, dtype=int)

id_counters = {}

# Criação da matriz
linhas = 3
colunas = 6

# Matriz 4x6 preenchida com zeros
matrix = [[0 for _ in range(colunas)] for _ in range(linhas)]

y1 = 78
y2 = 78 * 2
y3 = 234

x1 = 225
x2 = 225 * 2
x3 = 225 * 3
x4 = 225 * 4
x5 = 225 * 5
x6 = 1350

for row in data.itertuples(index=False):
    id_, x, y = row[0], row[1], row[2]
    valx = x - 312
    valy = y - 572

    posx = -1
    posy = -1

    if valy < y1:
        posy = 0
    elif valy < y2:
        posy = 1
    elif valy < y3:
        posy = 2

    if valx < x1:
        posx = 0
    elif valx <= x2:
        posx = 1
    elif valx <= x3:
        posx = 2
    elif valx <= x4:
        posx = 3
    elif valx <= x5:
        posx = 4
    elif valx <= x6:
        posx = 5

    if posy != -1 and posx != -1:
        matrix[posy][posx] += 1

# Encontrar os valores máximo e mínimo na matriz
matrixmax = max(max(row) for row in matrix)
matrixmin = min(min(row) for row in matrix)


som = matrixmax - matrixmin
div = som / 4

verde = div
amarelo = div * 2
laranja = div * 3
vermelho = matrixmax

# Inicializar a matriz de cores
matrixcores = [[0 for _ in range(colunas)] for _ in range(linhas)]

for linha in range(len(matrix)):
    for coluna in range(len(matrix[linha])):
        val = matrix[linha][coluna]
        if val == 0:
            matrixcores[linha][coluna] = -1
        elif val < verde:
            matrixcores[linha][coluna] = 0
        elif val < amarelo:
            matrixcores[linha][coluna] = 1
        elif val < laranja:
            matrixcores[linha][coluna] = 2
        else:
            matrixcores[linha][coluna] = 3

class VolleyballCourt:
    def __init__(self):
        self.length = 18  # comprimento
        self.width = 9    # largura
        self.divisions_x = 6  # número de divisões horizontais
        self.divisions_y = 3  # número de divisões verticais

    def draw(self, matrixcores, columns=None, save_path=None):
        fig, ax = plt.subplots(figsize=(12, 6))

        # Desenho do campo
        court = plt.Rectangle((0, 0), self.length, self.width, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(court)

        # Linha da Rede
        center_line = plt.Line2D([self.length / 2, self.length / 2], [0, self.width], linewidth=2.5, color='black')
        ax.add_line(center_line)

        # Divisão em linhas e colunas
        for i in range(1, self.divisions_x):
            ax.plot([i * self.length / self.divisions_x, i * self.length / self.divisions_x], [0, self.width], color='black', alpha=0)

        for i in range(1, self.divisions_y):
            ax.plot([0, self.length], [i * self.width / self.divisions_y, i * self.width / self.divisions_y], color='black', alpha=0)

        # Adicionando heatmap
        if matrixcores is not None:
            if columns is None:
                columns = range(self.divisions_x)
            for i in range(self.divisions_y):
                for j in columns:
                    color_val = matrixcores[i][j]
                    if color_val != -1:  # Ignorar quadrados com valor -1
                        color = self.get_color_from_value(color_val)  # Obtém a cor correspondente ao valor
                        ax.add_patch(plt.Rectangle((j * self.length / self.divisions_x, (self.divisions_y - i - 1) * self.width / self.divisions_y), self.length / self.divisions_x, self.width / self.divisions_y, facecolor=color, edgecolor='none'))

        ax.axis('off')

        plt.title('Heatmap')

        if save_path:
            plt.savefig(save_path)  # Salvar a figura se o caminho de salvamento for fornecido
        else:
            plt.show()

    def get_color_from_value(self, value):
        colors = {0: 'green', 1: 'yellow', 2: 'orange', 3: 'red', -1: 'white'}
        return colors.get(value, 'white')

