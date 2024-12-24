import random
import math
import matplotlib.pyplot as plt

# Параметры для экспериментов
p_values = [0.02, 0.05, 0.1]
field_sizes = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
num_experiments = 100000
q = 0.5  # МПа, значение по условию
missile_counts = [1, 3, 5, 10]  # Количество боеголовок
T_average_values = [15 / 60, 30 / 60]  # Время подлета (в часах)
V_approach_values = [30, 40, 50, 60]  # Скорость (км/ч)

def calculate_radius(p, q):
    """Формула для вычисления радиуса поражения"""
    k_c = 0.78 * p ** (-0.5)
    return k_c * q ** (1 / 3)

def calculate_distance(x1: float, y1: float, x2: float, y2: float):
    """Вычисляет расстояние между установкой и местом попадания ракеты"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def generate_point_in_circle(radius):
    """Генерация случайной точки в пределах круга с радиусом radius"""
    the_angle_at_which_the_point_lies = random.uniform(0, 2 * math.pi)  # Случайный угол
    r = random.uniform(0, radius)  # Случайное расстояние от центра
    x = r * math.cos(the_angle_at_which_the_point_lies)
    y = r * math.sin(the_angle_at_which_the_point_lies)
    return x, y

for T in T_average_values:
    for V in V_approach_values:
        z = V * T  # Радиус окружности размещения установки

        for missile_count in missile_counts:

            experimental_results = {}  # Словарь для хранения вероятностей попадания для каждого p
            theoretical_results = {}  # Теоретические данные

            for p in p_values:
                list_of_probabilities = []  # Вероятности для каждого размера поля
                destruction_radius = calculate_radius(p, q)  # Радиус поражения
                probabilities = []  # Список вероятностей для текущего p

                for field_size in field_sizes:
                    # Теоретическая вероятность
                    calculating_probability = (missile_count * (math.pi * destruction_radius ** 2) / field_size ** 2)
                    list_of_probabilities.append(calculating_probability)

                    hits = 0  # Количество попаданий

                    for _ in range(num_experiments):
                        # Генерация случайной установки в пределах круга радиуса z
                        installation_x, installation_y = generate_point_in_circle(z)

                        # Генерация мест падения ракет
                        places_of_impact = [(random.uniform(0, field_size), random.uniform(0, field_size))
                                            for _ in range(missile_count)]

                        # Проверка попадания
                        if any(
                                calculate_distance(installation_x, installation_y, missile_x, missile_y) <= destruction_radius
                                for missile_x, missile_y in places_of_impact
                        ):
                            hits += 1

                    # Рассчитываем вероятность попадания
                    probability = hits / num_experiments
                    probabilities.append(probability)

                # Сохраняем результаты
                experimental_results[p] = probabilities
                theoretical_results[p] = list_of_probabilities

            # Построение графиков
            for p, probabilities in experimental_results.items():
                plt.plot(field_sizes, probabilities, marker='o', linestyle='-', label=f'Экспериментальные, p = {p}')

            for p, list_of_probabilities in theoretical_results.items():
                plt.plot(field_sizes, list_of_probabilities, marker='x', linestyle='--', label=f'Теоретические, p = {p}')

            plt.xticks(field_sizes)
            plt.title(f"T={T * 60:.0f} мин, V={V} км/ч, {missile_count} боеголовок")
            plt.xlabel("Размер поля (field_size)")
            plt.ylabel("Вероятность поражения")
            plt.legend()
            plt.grid(True)
            plt.show()
