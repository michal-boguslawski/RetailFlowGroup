import importlib
import pkgutil
from pathlib import Path


def load_handlers(package_name: str = "generator.session.handlers") -> None:
    """Import every module in the handlers package so their @register_handler
    decorators run and populate the dispatch dict."""
    package = importlib.import_module(package_name)
    if package.__file__ is None:
        raise ImportError(f"Cannot locate package path for '{package_name}'")
    package_path = Path(package.__file__).parent

    for module_info in pkgutil.iter_modules([str(package_path)]):
        if module_info.name.startswith("_"):
            continue
        importlib.import_module(f"{package_name}.{module_info.name}")
