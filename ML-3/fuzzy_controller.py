class FuzzyController:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.rules = knowledge_base.get_rules()

    def tri(self, x, a, b, c):
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        else:
            return (c - x) / (c - b)

    def fuzz_passenger_flow(self, x):
        return {
            'Низкий': self.tri(x, 0, 20, 55),
            'Средний': self.tri(x, 40, 60, 85),
            'Высокий': self.tri(x, 70, 90, 100)
        }

    def fuzz_time_of_day(self, hour):
        return {
            'Ночь': self.tri(hour, 0, 3, 7),
            'Утро': self.tri(hour, 6, 9, 12),
            'День': self.tri(hour, 10, 14, 18),
            'Вечер': self.tri(hour, 17, 21, 24)
        }

    def defuzzify(self, activation):
        values = {
            'Мало активных': 1,
            'Норма активных': 2.5,
            'Много активных': 4
        }
        num, denom = 0.0, 0.0
        for term, val in activation.items():
            num += values[term] * (val ** 1.3)
            denom += val
        return num / denom if denom else 0

    def infer(self, passenger_flow, hour, verbose=False):
        f_flow = self.fuzz_passenger_flow(passenger_flow)
        f_time = self.fuzz_time_of_day(hour)
        activation = {
            'Мало активных': 0.0,
            'Норма активных': 0.0,
            'Много активных': 0.0
        }

        for rule in self.rules:
            mu_flow = f_flow.get(rule['flow'], 0)
            mu_time = f_time.get(rule['time'], 0)
            strength = min(mu_flow, mu_time)

            if strength > 0:
                activation[rule['action']] = max(activation[rule['action']], strength)
                if verbose:
                    print(
                        f"Правило ({rule['flow']} + {rule['time']} -> {rule['action']}) "
                        f"срабатывает со значением {strength:.2f}"
                    )

        if sum(activation.values()) == 0:
            activation['Мало активных'] = 0.2

        control = self.defuzzify(activation)
        return round(control, 2), activation
