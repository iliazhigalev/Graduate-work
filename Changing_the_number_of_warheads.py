import random
import math
import matplotlib.pyplot as plt

# Параметры для экспериментов
p_values = [0.02, 0.05, 0.1]
field_sizes = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
num_experiments = 100000
q = 0.5  # МПа, значение по условию
missile_counts = [1, 3, 5, 10]  # Количество боеголовок


def calculate_radius(p, q):
    """Формула для вычисления радиуса поражения"""
    k_c = 0.78 * p ** (-0.5)
    return k_c * q ** (1 / 3)


def calculate_distance(x1: float, y1: float, x2: float, y2: float):
    """Вычисляет расстояние между установкой и местом попадания ракеты"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


for missile_count in missile_counts:

    experimental_results = {}  # Словарь для хранения вероятностей попадания для каждого p для экспериментальных данных
    theoretical_results = {}  # Теоретические данные

    # Проведение экспериментов для каждого p и соответствующих размеров поля
    for p in p_values:

        list_of_probabilities = []  # Список с вероятностями и словарь с вероятностями одного p

        destruction_radius = calculate_radius(p, q)  # Вычисляем радиус поражения по формуле (1.2)

        probabilities = []  # список вероятностей для текущего p

        for field_size in field_sizes:

            # Вычисляем теоретическую вероятность
            calculating_probability = (missile_count * (math.pi * destruction_radius ** 2) / field_size ** 2)
            list_of_probabilities.append(calculating_probability)

            hits = 0  # количество попаданий

            for _ in range(num_experiments):
                # Случайное размещение установки и места падения ракеты
                installation_x, installation_y = random.uniform(0, field_size), random.uniform(0, field_size)

                # Генерируем количество попаданий в зависимости от количества боеголовок
                places_of_impact = [(random.uniform(0, field_size), random.uniform(0, field_size)) for _ in
                                    range(missile_count)]

                # Вычисляем расстояние между установкой и местом падения ракеты и если оно меньше радиуса поражения
                if any(
                        calculate_distance(installation_x, installation_y, missile_x, missile_y) <= destruction_radius
                        for missile_x, missile_y in places_of_impact
                ):
                    hits += 1

            # Рассчитываем вероятность попадания
            probability = hits / num_experiments
            probabilities.append(probability)

        # Сохраняем результаты для текущего p
        experimental_results[p] = probabilities
        theoretical_results[p] = list_of_probabilities

    # Экспериментальные данные
    for p, probabilities in experimental_results.items():
        plt.plot(field_sizes, probabilities, marker='o', linestyle='-', label=f'Экспериментальные данные, p = {p}')

    # Теоретические данные
    for p, list_of_probabilities in theoretical_results.items():
        plt.plot(field_sizes, list_of_probabilities, marker='x', linestyle='--', label=f'Аналитические данные, p = {p}')

    # Настройка графика
    plt.xticks(field_sizes)
    plt.title(f"Сравнение экспериментальной и аналитической вероятностей поражения для {missile_count} боеголовок")
    plt.xlabel("Размер поля (field_size)")
    plt.ylabel("Вероятность поражения")
    plt.legend()
    plt.grid(True)

    # Отображение графика
    plt.show()
