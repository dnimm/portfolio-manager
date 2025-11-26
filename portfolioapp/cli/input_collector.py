from rich.console import Console

_console = Console()

def collect_inputs(fields: dict) -> dict:
    data = {}
    for label, key in fields.items():
        data[key] = _console.input(f"{label}: ")
    return data
