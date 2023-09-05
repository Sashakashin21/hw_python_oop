class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.traning_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.traning_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_HOUR = 60
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / (self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self: str) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CONST: float = 0.035
    SECCONST: float = 0.029
    KOEF_SPEED_KMH_MS: float = 0.278
    SANT_METR: int = 100

    def __init__(self, action, duration, weight, height):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.CONST
             * self.weight
             + ((self.get_mean_speed()
                 * self.KOEF_SPEED_KMH_MS)**2
                 / (self.height / self.SANT_METR)) * self.SECCONST
                * self.weight) * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    CONST_SWIM: float = 1.1
    CONST_SPEED: int = 2
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        return (

            self.length_pool

            * self.count_pool

            / self.M_IN_KM

            / self.duration

        )

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CONST_SWIM) * self.CONST_SPEED
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict[str, type[Training]] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking}

    if workout_type not in workout:
        raise ValueError('Отстутствует тип тренировки')
    elif workout_type in workout:
        return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
