import random
import math
import matplotlib.pyplot as plt

# Параметры для экспериментов
p_values = [0.02, 0.05, 0.1]
num_experiments = 100000
q = 0.5  # МПа, значение по условию
missile_counts = [1, 3, 5, 10]  # Количество боеголовок
T_average_values = [15 / 60, 30 / 60]  # Время подлета (в часах)
V_approach_values = [30, 35, 40, 45, 50, 55, 60]  # Скорость (км/ч)


def calculate_radius(p, q):
    """Формула для вычисления радиуса поражения"""
    k_c = 0.78 * p ** (-0.5)
    return k_c * q ** (1 / 3)


def calculate_distance(x1: float, y1: float, x2: float, y2: float):
    """Вычисляет расстояние между установкой и местом попадания ракеты"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def generate_point_in_circle(radius):
    """Генерация случайной точки в пределах круга с радиусом radius"""
    angle = random.uniform(0, 2 * math.pi)  # Случайный угол
    r = random.uniform(0, radius)  # Случайное расстояние от центра
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    return x, y


for T in T_average_values:
    for missile_count in missile_counts:
        for p in p_values:
            destruction_radius = calculate_radius(p, q)  # Радиус поражения

            experimental_probabilities = []  # Для хранения экспериментальных вероятностей
            theoretical_probabilities = []  # Для хранения теоретических вероятностей

            for V in V_approach_values:
                z = V * T  # Радиус окружности размещения установки

                # Теоретическая вероятность для данного V
                theoretical_probability = (missile_count * (math.pi * destruction_radius ** 2)) / (math.pi * z ** 2)
                theoretical_probabilities.append(theoretical_probability)

                # Выполнение экспериментов
                hits = 0  # Количество попаданий

                for _ in range(num_experiments):
                    # Генерация случайной позиции установки
                    installation_x, installation_y = generate_point_in_circle(z)

                    # Генерация мест падения боеголовок
                    places_of_impact = [generate_point_in_circle(z) for _ in range(missile_count)]

                    # Проверка попаданий
                    if any(
                            calculate_distance(installation_x, installation_y, missile_x,
                                               missile_y) <= destruction_radius
                            for missile_x, missile_y in places_of_impact
                    ):
                        hits += 1

                # Рассчитываем вероятность попадания
                experimental_probability = hits / num_experiments
                experimental_probabilities.append(experimental_probability)

            # Построение графиков для данного p
            plt.plot(V_approach_values, experimental_probabilities, marker='o', linestyle='-',
                     label=f'Экспериментальные, p = {p}')
            plt.plot(V_approach_values, theoretical_probabilities, marker='x', linestyle='--',
                     label=f'Теоретические, p = {p}')

        plt.title(f"T={T * 60:.0f} мин, {missile_count} боеголовок")
        plt.xlabel("Скорость (V), км/ч")
        plt.ylabel("Вероятность поражения")
        plt.legend()
        plt.grid(True)
        plt.show()
