import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Definir a matriz fornecida
matrix = np.array([
    [0.82212908, 0.9505332, 0.74354319, 0.62732901, 0.80625566, 0.38619353],
    [0.45649156, 0.34671052, 0.6489444, 0.95727833, 0.96583984, 0.19575295],
    [0.48118427, 0.09939401, 0.04387482, 0.77030369, 0.73326068, 0.28080632],
    [0.83253029, 0.32500029, 0.05888976, 0.15285764, 0.77647455, 0.16901722]
])

# Obter a paleta de cores "YlOrRd" com 10 cores
palette = sns.color_palette("YlOrRd", 10)

# Normalizar os valores da matriz para o intervalo de 0 a 1
norm_matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

# Mapear os valores normalizados para índices da paleta de cores
color_indices = (norm_matrix * (len(palette) - 1)).astype(int)

# Criar uma matriz de cores correspondente
color_matrix = np.array([[palette[idx] for idx in row] for row in color_indices])

# Plotar a matriz de cores
plt.imshow(color_matrix, aspect='auto')
plt.colorbar()  # Adicionar uma barra de cores para referência
plt.title("Matrix Colored with 'YlOrRd' Palette")
plt.show()
