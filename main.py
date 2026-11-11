import sys
from pathlib import Path
from dotenv import load_dotenv
from src.app import create_app
import os


def get_resources_and_styles_dir():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def init_env(app_dir):
    env_path = app_dir / ".env"

    if not env_path.exists():
        env_path.write_text("YANDEX_MAPS_API_KEY=\nYANDEX_GEOCODER_API_KEY=", encoding="utf-8")
        return '', ''

    load_dotenv(dotenv_path=env_path)
    MAPS_API_KEY = os.getenv("YANDEX_MAPS_API_KEY", "")
    GEOCODER_API_KEY = os.getenv("YANDEX_GEOCODER_API_KEY", "")
    return MAPS_API_KEY, GEOCODER_API_KEY



if __name__ == '__main__':
    res_dir = get_resources_and_styles_dir()
    app_dir = get_app_dir()
    icon_path = res_dir / "resources" / "icon.png"
    settings_icon_path = res_dir / "resources" / "settings.png"
    style_path = res_dir / "styles" / "style.qss"
    MAPS_API_KEY, GEOCODER_API_KEY = init_env(app_dir)
    app, window = create_app(icon_path, settings_icon_path, style_path, MAPS_API_KEY, GEOCODER_API_KEY)
    window.show()
    sys.exit(app.exec())