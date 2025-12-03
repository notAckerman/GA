import numpy as np
import matplotlib.pyplot as plt


def trapezoidal_mf(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c)
    return 0.0


def compute_membership(value, sets):
    memberships = {}
    for name, params in sets.items():
        memberships[name] = trapezoidal_mf(value, *params)
    return memberships


def plot_fuzzy_sets(x_harvest, harvest_sets, x_soil, soil_sets):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for name, params in harvest_sets.items():
        y = [trapezoidal_mf(xx, *params) for xx in x_harvest]
        axes[0].plot(x_harvest, y, label=name)
    axes[0].set_title("Время сбора урожая")
    axes[0].set_xlabel("Дни сезона")
    axes[0].set_ylabel("Степень принадлежности")
    axes[0].legend()
    axes[0].grid(True)

    for name, params in soil_sets.items():
        y = [trapezoidal_mf(xx, *params) for xx in x_soil]
        axes[1].plot(x_soil, y, label=name)
    axes[1].set_title("Плодородность почвы")
    axes[1].set_xlabel("Уровень (%)")
    axes[1].set_ylabel("Степень принадлежности")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


def main():
    harvest_sets = {
        "Раннее": (0, 0, 20, 40),
        "Среднее": (30, 45, 55, 70),
        "Позднее": (60, 80, 100, 100)
    }

    soil_sets = {
        "Низкий": (0, 0, 20, 40),
        "Средний": (30, 45, 55, 70),
        "Высокий": (60, 80, 100, 100)
    }

    x_harvest = np.linspace(0, 100, 500)
    x_soil = np.linspace(0, 100, 500)

    try:
        harvest_value = float(input("Введите количество дней до сбора урожая: "))
        soil_value = float(input("Введите уровень плодородности почвы (%): "))
    except ValueError:
        print("Ошибка ввода! Введите числовые значения.")
        return

    harvest_memberships = compute_membership(harvest_value, harvest_sets)
    soil_memberships = compute_membership(soil_value, soil_sets)

    print("\nСтепень принадлежности (время сбора урожая):")
    for name, degree in harvest_memberships.items():
        print(f"{name:10s} -> {degree:.2f}")

    print("\nСтепень принадлежности (плодородность почвы):")
    for name, degree in soil_memberships.items():
        print(f"{name:10s} -> {degree:.2f}")

    plot_fuzzy_sets(x_harvest, harvest_sets, x_soil, soil_sets)

if __name__ == "__main__":
    main()
