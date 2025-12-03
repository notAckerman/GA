import random
import time

class ElevatorSimulator:
    def __init__(self, controller, hours=24):
        self.controller = controller
        self.hours = hours
        self.results = []

    def run(self):
        print("Запуск симуляции...")
        for hour in range(self.hours):
            flow = random.randint(0, 100)
            control, activation = self.controller.infer(flow, hour)
            self.results.append({
                "hour": hour,
                "flow": flow,
                "control": control,
                "activation": activation
            })
            time.sleep(1)
            print(f"{hour:02d}:00  flow={flow:3d}  control={control:.2f}  {activation}")
        print("Симуляция завершена.")
        return self.results
