from dependency_injector import containers, providers

class ServiceWrappingMeta(containers.DeclarativeContainer.__class__):
    """Metaclass tự động wrap các provider *_service."""

    def __new__(cls, name, bases, namespace, **kwargs):
        injected_func_name = kwargs.pop("injected_func_name", None)

        _cls = super().__new__(cls, name, bases, namespace, **kwargs)

        # Tìm lớp Container cha
        parent_container = None
        for base in bases:
            if issubclass(base.__class__, containers.DeclarativeContainer.__class__):
                parent_container = base
                break

        if not parent_container:
            return _cls

        if injected_func_name:
            # Lấy hàm inject user khai báo trong namespace hoặc kế thừa
            inject_func = namespace.get(injected_func_name) or getattr(_cls, injected_func_name)

            # Tự động wrap mọi provider có hậu tố _service từ Container cha
            for attr_name, provider in parent_container.providers.items():
                if attr_name.endswith("_service"):
                    wrapped = providers.Callable(inject_func, provider, _cls.api_invoker)
                    setattr(_cls, attr_name, wrapped)

        return _cls
