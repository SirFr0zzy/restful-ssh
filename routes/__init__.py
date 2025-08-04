import importlib
import pathlib
from flask import Blueprint
from os import getenv


def register_routes(app):
    base = pathlib.Path(__file__).parent
    base_pkg = __package__  # z. B. "routes"

    def print_route_registration(modulename, route):
        max_width = 80  # Breite bis zu den URLs
        dots = "." * max(1, max_width - len(modulename) - 2)
        print(f"\033[92m✅\033[0m Route registered: {modulename} {dots} {route}")

    for path in base.rglob("*.py"):
        if path.name == "__init__.py":
            continue

        relative = path.relative_to(base.parent).with_suffix("")
        modulename = ".".join(relative.parts)

        try:
            module = importlib.import_module(modulename)
        except Exception as e:
            print(f"❌ Fehler beim Importieren von {modulename}: {e}")
            continue

        for obj in vars(module).values():
            if isinstance(obj, Blueprint):
                try:
                    app.register_blueprint(obj, url_prefix=getenv("ROUTE_PREFIX"))
                    print_route_registration(modulename, obj.name)
                except Exception as e:
                    print(f"❌ Fehler beim Registrieren von {modulename}: {e}")