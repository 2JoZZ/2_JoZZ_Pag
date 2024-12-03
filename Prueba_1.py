# Importamos las librerías necesarias para trabajar con archivos ZIP y para graficar
import random  # Para generar números aleatorios
import zipfile  # Para trabajar con archivos comprimidos ZIP
import matplotlib.pyplot as plt  # Para graficar las posiciones mutadas


# Función para leer una secuencia de ADN desde un archivo FNA dentro de un archivo ZIP
def read_fna_from_zip(zip_file_name, fna_file_name):
    sequence = ""  # Iniciamos una variable vacía para almacenar la secuencia

    # Abrimos el archivo ZIP
    with zipfile.ZipFile(zip_file_name, 'r') as zip_file:
        with zip_file.open(fna_file_name) as file:
            for line in file:    # Para leer cada linea del archivo
                line = line.decode('utf-8')  # Decodificamos la línea de bytes a texto
                if not line.startswith(">"):  # tambien sirve para ignorar la primera linea que es el titulo
                    sequence += line.strip()  # se agrega la secuencia de ADN

    return sequence.upper()  # para asegurar que toda la secuencia se encuentre en mayuscula


# Función que use para introducir las mutaciones
def mutate_sequence(sequence, num_mutations=1):
    sequence = list(sequence)  # toca crear una lista para poder manejar la secuencia
    bases = ['A', 'T', 'C', 'G']  # aqui se especifican las posible mutaciones que son añadir o cambiar una base por otra
    mutations = []  # aqui se guardan las mutaciones creadas, esto es una lista

    # Aplicación de la mutaciones
    for _ in range(num_mutations):
        pos = random.randint(0, len(sequence) - 1)  # con esto se selecciona una secuencia aleatoria (aqui busque como poder hacerlo porque los otros que vimos no queria funcionarme)
        original_base = sequence[pos]  # aqui se guarda ña base nitrogenada original
        new_base = random.choice([b for b in bases if b != original_base])  # con esto se elige alguna de las opciones de bases nitrogenadas para hacer el cambio
        sequence[pos] = new_base  # esta linea realiza la sustitucion de la base por la de mutacion
        mutations.append((pos, original_base, new_base))  # y se guarda la mutacion
    return ''.join(sequence), mutations  # Devolvemos la secuencia mutada y la lista de mutaciones realizadas


# Graficas
def plot_mutations(sequence, mutations):
    mutated_positions = [0] * len(
        sequence)  # se inicia una lista con ceros, para representar las posiciones no mutadas

    for pos, _, _ in mutations:
        mutated_positions[pos] = 1  # Cambiamos el valor en las posiciones mutadas a 1

    # Grafica de barras
    plt.figure(figsize=(10, 2))  # tamaño
    plt.bar(range(len(sequence)), mutated_positions, color='red',
            label='Posiciones Mutadas')  # la barra en rojo corresponde a las mutaciones
    plt.title("Distribución de Mutaciones en la Secuencia")  # Título
    plt.xlabel("Posición en la Secuencia")  # Posicion de la secuencia
    plt.ylabel("Mutación (0 = No, 1 = Sí)")  # 0 = no mutada, 1 = mutada
    plt.legend()
    plt.show()  # Mostramos la gráfica


# Función
if __name__ == "__main__":
    zip_file_name = "lacZ_datasets.zip"  # Nombre del archivo ZIP que contiene la secuencia
    fna_file_name = "ncbi_dataset/data/gene.fna"  # Ruta del archivo FNA dentro del ZIP
    num_mutations = 5  # Número de mutaciones

    # Leemos la secuencia desde el archivo FNA dentro del ZIP
    sequence = read_fna_from_zip(zip_file_name, fna_file_name)
    print("Secuencia Original:")
    print(sequence)
    mutated_sequence, mutations = mutate_sequence(sequence, num_mutations)
    print("\nSecuencia Mutada:")
    print(mutated_sequence) #reporte de mutaciones
    print("\nMutaciones Realizadas:")
    for mut in mutations:
        print(f"Posición {mut[0]}: {mut[1]} → {mut[2]}")  # Mostramos la posición, base original y nueva base
    plot_mutations(sequence, mutations) # se grafican las mutaciones
