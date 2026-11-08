from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
import os
import json
import sys
from dotenv import load_dotenv
from src.translations import STRINGS


load_dotenv()
API_KEY = os.getenv("YANDEX_MAPS_API_KEY", "")
GEOCODER_API_KEY = os.getenv("YANDEX_GEOCODER_API_KEY", "")


class MapBridge(QObject):
    pointClicked = pyqtSignal(float, float, str)
    markerRightClicked = pyqtSignal(int)

    @pyqtSlot(float, float, str)
    def receive_coords_and_address(self, lat, lng, address):
        self.pointClicked.emit(lat, lng, address)

    @pyqtSlot(int)
    def receive_marker_id(self, loc_id):
        self.markerRightClicked.emit(loc_id)


os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"


class MapWidget(QWidget):
    sig_clicked = pyqtSignal(float, float, str)
    sig_right_clicked = pyqtSignal(int)
    def __init__(self, parent=None, current_language="English"):
        super().__init__(parent)
        self.current_language = current_language
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.channel = QWebChannel()
        self.bridge = MapBridge()

        self.bridge.pointClicked.connect(self.sig_clicked)
        self.bridge.markerRightClicked.connect(self.sig_right_clicked)

        self.channel.registerObject("pyBridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

    def contextMenuEvent(self, event):
        event.accept()

    def render_map(self, locations=None):
        yandex_lang = "en_US" if self.current_language == "English" else "ru_RU"
        if not locations:
            locations = []
            start_lat, start_lng = 55.75583, 37.6173
            zoom = 10
        else:
            start_lat = locations[0]["lat"]
            start_lng = locations[0]["lng"]
            zoom = 10

        locations_json = json.dumps(locations, ensure_ascii=False)

        html_data = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <style>
                html, body, #map {{ width: 100%; height: 100%; padding: 0; margin: 0; }}
                .marker {{
                    width: 16px;
                    height: 16px;
                    background: #e53935;
                    border: 2px solid #fff;
                    border-radius: 50%;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.5);
                    cursor: pointer;
                    transition: transform 0.15s ease;
                }}
                .marker:hover {{
                    transform: scale(1.3);
                }}
                .marker.active {{
                    background: #1e88e5;
                    box-shadow: 0 0 0 4px rgba(30,136,229,0.35), 0 1px 4px rgba(0,0,0,0.5);
                }}
            </style>
            <script src="https://api-maps.yandex.ru/v3/?apikey={API_KEY}&lang={yandex_lang}"></script>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        </head>
        <body>
            <div id="map"></div>
            <div id="info-panel" style="
                display: none; position: absolute; top: 10px; right: 10px;
                background: white; padding: 12px 30px 12px 12px; border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3); z-index: 1000;
                font-size: 14px; min-width: 150px;
            ">
                <span id="info-close" style="
                    position: absolute; top: 6px; right: 10px;
                    cursor: pointer; font-size: 18px, line-height: 1;
                    color: #888; user-select: none;
                ">&times;</span>
                <b id="info-name"></b><br>
                <span id="info-address"></span><br>
                <span id="info-coords"></span>
            </div>
            <div id="search-panel" style="
                position: absolute; top: 10px; left: 10px; z-index: 1000;
                display: flex; gap: 4px;
            ">
                <input id="search-input" type="text"
                    style="padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px; width: 220px; font-size: 14px;">
                <button id="search-btn" style="
                    padding: 6px 12px; border: none; background: #1e88e5;
                    color: white; border-radius: 4px; cursor: pointer; font-size: 14px;
                "></button>
            </div>
            <script>
                var bridge;
                const LOCATIONS = {locations_json};

                new QWebChannel(qt.webChannelTransport, function (channel) {{
                    bridge = channel.objects.pyBridge;
                }});

                document.addEventListener('contextmenu', e => e.preventDefault());
                
                document.getElementById('info-close').addEventListener('click', (e) => {{
                    e.stopPropagation();
                    document.getElementById('info-panel').style.display = 'none';
                    document.querySelectorAll('.marker.active').forEach((m) => m.classList.remove('active'));
                }});
                
                async function getAddressByCoords(lat, lng) {{
                    const url = `https://geocode-maps.yandex.ru/v1/?apikey={GEOCODER_API_KEY}&geocode=${{lng}},${{lat}}&format=json&results=1`;
                    try {{
                        const response = await fetch(url);
                        const data = await response.json();
                        const members = data.response.GeoObjectCollection.featureMember;
                        if (members && members.length > 0) {{
                            return members[0].GeoObject.metaDataProperty.GeocoderMetaData.text;
                        }}
                        return "";
                    }}
                    catch (err) {{
                        return "";
                    }}
                }}
                
                async function doSearch() {{
                    const text = document.getElementById('search-input').value.trim();
                    if (!text) return;
                
                    try {{
                        const url = `https://geocode-maps.yandex.ru/v1/?apikey={GEOCODER_API_KEY}&geocode=${{encodeURIComponent(text)}}&format=json&results=1`;
                        const response = await fetch(url);
                        const data = await response.json();
                
                        const members = data.response.GeoObjectCollection.featureMember;
                        if (members && members.length > 0) {{
                            const geoObject = members[0].GeoObject;
                            const pos = geoObject.Point.pos;
                            const [lng, lat] = pos.split(' ').map(Number);
                
                            window._map.setLocation({{
                                center: [lng, lat],
                                zoom: 15
                            }});
                        }} else {{
                            alert("{STRINGS[self.current_language]["map_nothing_found"]}");
                        }}
                    }} catch (err) {{
                        alert("{STRINGS[self.current_language]["invalid_geocoder_api_key"]}");
                    }}
                }}
                
                document.getElementById('search-btn').addEventListener('click', doSearch);
                document.getElementById('search-input').addEventListener('keydown', (e) => {{
                    if (e.key === 'Enter') doSearch();
                }});
                
                function setActiveMarker(el) {{
                    document.querySelectorAll('.marker.active').forEach((m) => m.classList.remove('active'));
                    el.classList.add('active');
                }}

                async function initMap() {{
                    await ymaps3.ready;
                    document.getElementById('search-input').placeholder = "{STRINGS[self.current_language]["default_search"]}";
                    document.getElementById('search-btn').textContent = "{STRINGS[self.current_language]["btn_search"]}";
                    const {{ YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapMarker, YMapListener }} = ymaps3;

                    const map = new YMap(document.getElementById('map'), {{
                        location: {{
                            center: [{start_lng}, {start_lat}],
                            zoom: {zoom}
                        }},
                        behaviors: ['drag', 'scrollZoom', 'pinchZoom', 'dblClick']
                    }});
                    window._map = map;

                    map.addChild(new YMapDefaultSchemeLayer());
                    map.addChild(new YMapDefaultFeaturesLayer());

                    map.addChild(new YMapListener({{
                        layer: 'any',
                        onClick: async (object, event) => {{
                            if (object) {{
                                return;
                            }}
                            const lat = event.coordinates[1];
                            const lng = event.coordinates[0];
                            const address = await getAddressByCoords(lat, lng);
                            if (bridge) {{
                                bridge.receive_coords_and_address(lat, lng, address);
                            }}
                        }}
                    }}));

                    LOCATIONS.forEach((loc) => {{
                        const el = document.createElement('div');
                        el.className = 'marker';

                        el.addEventListener('contextmenu', (e) => {{
                            e.preventDefault();
                            e.stopPropagation();
                            if (bridge) {{
                                bridge.receive_marker_id(loc.id);
                            }}
                        }});
                        
                        if (LOCATIONS.length > 0) {{
                            let minLng = LOCATIONS[0].lng, maxLng = LOCATIONS[0].lng;
                            let minLat = LOCATIONS[0].lat, maxLat = LOCATIONS[0].lat;
                        
                            LOCATIONS.forEach((loc) => {{
                                if (loc.lng < minLng) minLng = loc.lng;
                                if (loc.lng > maxLng) maxLng = loc.lng;
                                if (loc.lat < minLat) minLat = loc.lat;
                                if (loc.lat > maxLat) maxLat = loc.lat;
                            }});
                        
                            // API 3.0: bounds = [[minLng, minLat], [maxLng, maxLat]]
                            map.setLocation({{
                                bounds: [[minLng, minLat], [maxLng, maxLat]]
                            }});
                        }}

                        const marker = new YMapMarker(
                            {{ coordinates: [loc.lng, loc.lat],
                               position: 'center',
                                onClick: () => {{
                                    setActiveMarker(el);
                                    document.getElementById('info-name').textContent = loc.name;
                                    document.getElementById('info-address').textContent = loc.address || '';
                                    document.getElementById('info-coords').textContent =
                                        `lat: ${{loc.lat.toFixed(5)}}, lng: ${{loc.lng.toFixed(5)}}`;
                                    document.getElementById('info-panel').style.display = 'block';
                                }}
                            }},
                            el
                        );
                        map.addChild(marker);
                    }});
                }}

                window.onload = initMap;
            </script>
        </body>
        </html>
        """
        self.browser.setHtml(html_data, QUrl("http://localhost/"))

    def clear_map(self):
        html_data = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <style>
                html, body {{
                    width: 100%; height: 100%; padding: 0; margin: 0;
                    background-color: #f4f9ee;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body></body>
        </html>
        """
        self.browser.setHtml(html_data, QUrl("http://localhost/"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = QMainWindow()
    map_widget = MapWidget()

    map_widget.sig_clicked.connect(lambda lat, lng: print(f"Клик в Python: {lat}, {lng}"))

    main_win.setCentralWidget(map_widget)
    main_win.resize(800, 600)
    main_win.show()
    map_widget.render_map([
        {"id": 1, "lat": 55.75583, "lng": 37.6173, "name": "Москва", "address": "Красная Площадь"},
    ])
    #map_widget.render_map()
    sys.exit(app.exec())