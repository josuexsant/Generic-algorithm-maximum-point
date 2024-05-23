import socket
import pickle
import numpy as np
import math
import threading
import matplotlib
matplotlib.use('Agg')  # Usamos 'Agg' para modo no interactivo
import matplotlib.pyplot as plt
import io
import tempfile
from guizero import App, Text, PushButton, Picture
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def fx(x):
    return -(0.1 + (1 - x)**2 - 0.1 * math.cos(6 * math.pi * (1 - x))) + 2

def plot_points():
    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis, color='black')
    for i, (x, y) in enumerate(client_points):
        ax.plot(x, y, 'o', label=f'Cliente {i+1}')
    if client_points:
        max_point = max(client_points, key=lambda p: p[1])
        ax.plot(max_point[0], max_point[1], 'ro', label='Mejor Punto')
    ax.set_title('Datos de los clientes')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    ax.grid(True)
    
    # Crear un directorio temporal personalizado
    with tempfile.TemporaryDirectory() as tmpdirname:
        filepath = f"{tmpdirname}/plot.png"
        fig.savefig(filepath, format='png')
        plot_image.value = filepath

HOST = '192.168.1.70'
PORT = 65123
client_points = []  # Lista para almacenar los puntos de los clientes

app = App(title="Servidor", layout="grid")

Text(app, text="Datos de los clientes:", grid=[0, 0])

plot_image = Picture(app, image=None, grid=[0, 1])

def start_server_thread():
    def start_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            server_status.value = "Servidor esperando conexiones..."

            while True:
                conn, addr = s.accept()
                with conn:
                    server_status.value = f'Conexión establecida desde {addr}'
                    
                    data = conn.recv(4096)
                    if not data:
                        server_status.value = "No se han recibido datos del cliente."
                        continue
                    
                    best_individual_decimal, best_individual_fitness = pickle.loads(data)
                    server_status.value = f'Datos recibidos del cliente - Decimal: {best_individual_decimal}, Fitness: {best_individual_fitness}'

                    # Almacenar los puntos del cliente en la lista
                    client_points.append((best_individual_decimal, best_individual_fitness))
                    
                    # Actualizar la gráfica
                    plot_points()

    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

server_status = Text(app, text="Esperando conexiones...", grid=[0, 2])

start_button = PushButton(app, command=start_server_thread, text="Iniciar servidor", grid=[0, 3])

x_axis = np.arange(0, 2, 0.02)
y_axis = [fx(num) for num in x_axis]

app.display()