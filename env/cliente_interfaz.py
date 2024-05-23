import socket
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math
from guizero import App, PushButton, Text

# Configuración del cliente
HOST = '169.254.74.37'
PORT = 65123

def fx(x):
    return -(0.1 + (1 - x)**2 - 0.1 * math.cos(6 * math.pi * (1 - x))) + 2

def listToDecimal(num):
    decimal = 0
    for i in range(len(num)):
        decimal += num[i] * 10**(-i)
    return decimal

def mutate(individuals, prob, pool):
    for i in range(len(individuals)):
        mutate_individual = individuals[i]
        if np.random.random() < prob:
            mutation = np.random.choice(pool[0])
            mutate_individual = [mutation] + mutate_individual[1:]
        
        for j in range(1, len(mutate_individual)):
            if np.random.random() < prob:
                mutation = np.random.choice(pool[1])
                mutate_individual = mutate_individual[0:j] + [mutation] + mutate_individual[j + 1:]
        individuals[i] = mutate_individual

def run_genetic_algorithm(poblacion):
    generaciones = 10

    for gen in range(generaciones):
        fitness = []
        for individuo in poblacion:
            x = listToDecimal(individuo)
            y = fx(x)
            fitness.append(y)
        
        fitness = np.array(fitness)
        fitness = fitness / fitness.sum()
        
        offspring = []
        for i in range(len(poblacion) // 2):
            parents = np.random.choice(len(poblacion), 2, p=fitness)
            cross_point = np.random.randint(ind_size)
            offspring.append(poblacion[parents[0]][:cross_point] + poblacion[parents[1]][cross_point:])
            offspring.append(poblacion[parents[1]][:cross_point] + poblacion[parents[0]][cross_point:])
        
        poblacion = offspring
        
        mutate(poblacion, 0.005, genetic_pool)

    x_axis = np.arange(0, 2, 0.02)
    y_axis = [fx(num) for num in x_axis]

    best_individual_index = np.where(fitness == fitness.max())[0][0]
    best_individual_decimal = listToDecimal(poblacion[best_individual_index])
    best_individual_fitness = fx(best_individual_decimal)

    print(f"Mejor individuo: {best_individual_decimal}")
    print(f"Valor de la función: {best_individual_fitness}")

    data = pickle.dumps((best_individual_decimal, best_individual_fitness))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data)
        print("Datos enviados al servidor.")

    # Devolver los valores calculados
    return best_individual_decimal, best_individual_fitness

# Inicialización de la población
ind_size = 15
genetic_pool = [[0, 1], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
poblacion = []
for i in range(100):
    individuo = [np.random.choice(genetic_pool[0])]
    individuo += list(np.random.choice(genetic_pool[1], ind_size - 1))
    poblacion.append(individuo)

# Creación de la interfaz gráfica
app = App(title="Algoritmo Genético")

def start_algorithm():
    # Llamar a la función run_genetic_algorithm con poblacion como argumento
    best_individual_decimal, best_individual_fitness = run_genetic_algorithm(poblacion)
    result_text.value = f"Mejor individuo: {best_individual_decimal}\nValor de la función: {best_individual_fitness}"
    
start_button = PushButton(app, command=start_algorithm, text="Iniciar Algoritmo")
result_text = Text(app, text="")

app.display()