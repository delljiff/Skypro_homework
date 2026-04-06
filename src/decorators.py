from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Логирует успешные вызовы и ошибки в консоль или файл.

    Параметры:
        filename (Optional[str]): Имя файла для записи логов.
                                   Если None — логи выводятся в консоль.

    Возвращает:
        Callable: Декоратор функции.

    Пример:
        @log()
        def add(a, b):
            return a + b

        @log(filename="log.txt")
        def div(a, b):
            return a / b
    """

    def decorator(func: Callable) -> Callable:
        """
        Внутренний декоратор, принимающий функцию.

        Параметры:
            func (Callable): Декорируемая функция.

        Возвращает:
            Callable: Функция-обёртка.
        """

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Обёртка, выполняющая логирование.

            Параметры:
                *args (Any): Позиционные аргументы функции.
                **kwargs (Any): Именованные аргументы функции.

            Возвращает:
                Any: Результат вызова функции.

            Исключения:
                Exception: Пробрасывает исключения, возникшие в функции.
            """
            try:
                result = func(*args, **kwargs)
                msg = f"{func.__name__} ok"
            except Exception as e:
                msg = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                raise
            finally:
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(msg + "\n")
                else:
                    print(msg)
            return result

        return wrapper

    return decorator
