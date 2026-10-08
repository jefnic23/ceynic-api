import subprocess

import typer

from src.utils.generate_frontend_models import generate_frontend_models

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Ceynic backend development commands."""


@app.command("generate-frontend-models")
def generate_frontend_models_command() -> None:
    """Generate frontend schemas and TypeScript models."""
    try:
        generate_frontend_models()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error


if __name__ == "__main__":
    app()
