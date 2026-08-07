import sys
from pathlib import Path
from src.app import create_app


if __name__ == '__main__':
    icon_path = Path(__file__).resolve().parent / "resources" / "icon.png"
    app, window = create_app(icon_path)
    window.show()
    sys.exit(app.exec())