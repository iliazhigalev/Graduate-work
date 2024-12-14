import random
import math
import matplotlib.pyplot as plt

# Параметры для экспериментов
p_values = [0.02, 0.05, 0.1]
field_sizes = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
num_experiments = 100000
q = 0.5  # МПа, значение по условию

probabilities_for_plotting = {}

def calculate_radius(p, q):
    """Формула для вычисления радиуса поражения"""
    k_c = 0.78 * p ** (-0.5)
    return k_c * q ** (1 / 3)


def calculate_distance(x1: float, y1: float, x2: float, y2: float):
    """Вычисляет расстояние между установкой и местом попадания ракеты"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Словарь для хранения вероятностей попадания для каждого p
results = {}

# Проведение экспериментов для каждого p и соответствующих размеров поля
for p in p_values:
    # Список с вероятностями и словарь с вероятностями одного p
    P_list = []
    # Вычисляем радиус поражения по формуле (1.2)
    destruction_radius = calculate_radius(p, q)

    probabilities = []  # список вероятностей для текущего p

    for field_size in field_sizes:
        # Вычисляем теоретическую вероятность
        calculating_probability = (math.pi * destruction_radius ** 2) / field_size ** 2
        P_list.append(calculating_probability)

        hits = 0  # количество попаданий

        for _ in range(num_experiments):
            # Случайное размещение установки и места падения ракеты
            installation_x, installation_y = random.uniform(0, field_size), random.uniform(0, field_size)
            missile_x, missile_y = random.uniform(0, field_size), random.uniform(0, field_size)

            # Вычисляем расстояние между установкой и местом падения ракеты
            distance = calculate_distance(installation_x, installation_y, missile_x, missile_y)

            # Проверка попадания
            if distance <= destruction_radius:
                hits += 1

        # Рассчитываем вероятность попадания
        probability = hits / num_experiments
        probabilities.append(probability)

    # Сохраняем результаты для текущего p
    results[p] = probabilities
    probabilities_for_plotting[p] = P_list

# Экспериментальные данные
for p, probabilities in results.items():
    plt.plot(field_sizes, probabilities, marker='o', linestyle='-', label=f'Экспериментальные данные, p = {p}')

# Теоретические данные
for p, P_list in probabilities_for_plotting.items():
    plt.plot(field_sizes, P_list, marker='x', linestyle='--', label=f'Теоретические данные, p = {p}')

# Настройка графика
plt.xticks(field_sizes)
plt.title("Сравнение экспериментальных и теоретических вероятностей поражения")
plt.xlabel("Размер поля (field_size)")
plt.ylabel("Вероятность поражения")
plt.legend()
plt.grid(True)

# Отображение графика
plt.show()