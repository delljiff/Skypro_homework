from typing import Optional, Any, Callable


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Параметры:
        filename (Optional[str]): Имя файла для записи логов.
                                   Если None — логи выводятся в консоль.

    Возвращает:
        Callable: Декоратор функции.
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
                msg = f"OK: {func.__name__}{args}{kwargs} = {result}"
            except Exception as e:
                msg = f"ERROR: {func.__name__}{args}{kwargs} -> {type(e).__name__}"
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
