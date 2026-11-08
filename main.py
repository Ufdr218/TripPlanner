import sys
from pathlib import Path
from src.app import create_app


if __name__ == '__main__':
    icon_path = Path(__file__).resolve().parent / "resources" / "icon.png"
    settings_icon_path = Path(__file__).resolve().parent / "resources" / "settings.png"
    style_path = Path(__file__).resolve().parent / "styles" / "style.qss"
    app, window = create_app(icon_path, settings_icon_path, style_path)
    window.show()
    sys.exit(app.exec())