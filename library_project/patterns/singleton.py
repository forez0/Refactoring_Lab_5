"""Модуль, що реалізує патерн Singleton через метаклас."""

class SingletonMeta(type):
    """Метаклас для реалізації патерна Singleton.

    Забезпечує створення лише одного екземпляру класу.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Повертає єдиний екземпляр класу, створюючи його при першому виклику.

        Якщо екземпляр вже існує, повертає його замість створення нового.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
