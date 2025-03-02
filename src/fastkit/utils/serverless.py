from functools import wraps
from typing import Type, List, Dict, Any
from inspect import signature

class Provide:
    """Аналог FastAPI Depends для сервисов."""

    def __init__(self, service_type: Type):
        self.service_type = service_type

    def resolve(self, service_container):
        """Возвращает сервис, если он зарегистрирован в @serverless."""
        return service_container.get(self.service_type)


def serverless(services: List[Type]):
    """Декоратор для автоматического DI сервисов."""

    def decorator(cls):
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self, db_session, *args, **kwargs):
            self.db_session = db_session
            self._service_container: Dict[Type, Any] = {}

            # Автоматически создаем сервисы и кладем их в контейнер
            for service in services:
                self._service_container[service] = service(db_session)

            original_init(self, db_session, *args, **kwargs)

        def get_service(self, service_type: Type):
            """Возвращает сервис из контейнера."""
            return self._service_container.get(service_type)

        cls.__init__ = new_init
        cls.get_service = get_service
        return cls

    return decorator


def serviceable(func):
    """Декоратор для автоматического внедрения зависимостей в методы."""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        sig = signature(func)
        params = sig.parameters

        for param_name, param in params.items():
            if isinstance(param.default, Provide) and param_name not in kwargs:
                kwargs[param_name] = param.default.resolve(
                    self._service_container)

        return await func(self, *args, **kwargs)

    return wrapper
