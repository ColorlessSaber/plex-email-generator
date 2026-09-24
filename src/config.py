from pathlib import Path

PROJECT_DIR = (
    Path(__file__).resolve().parent.parent
)  # first parent is src/ next is the main project folder
ASSETS_DIR = PROJECT_DIR / "assets"
POSTERS_DIR = PROJECT_DIR / "data" / "posters"
HTML_DIR = PROJECT_DIR / "data" / "html"