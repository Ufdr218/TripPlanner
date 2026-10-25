from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import folium
import os
import json


class MapBridge(QObject):
    pointClicked = pyqtSignal(float, float)
    markerRightClicked = pyqtSignal(int)

    @pyqtSlot(float, float)
    def receive_coords(self, lat, lng):
        self.pointClicked.emit(lat, lng)

    @pyqtSlot(int)
    def receive_marker_id(self, loc_id):
        self.markerRightClicked.emit(loc_id)


os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"


class MapWidget(QWidget):
    sig_clicked = pyqtSignal(float, float)
    sig_right_clicked = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.browser.setHtml("")
        if not locations:
            locations = []
            start_lat, start_lng = 48.8566, 2.3522
            zoom = 2
        else:
            start_lat = locations[0]["lat"]
            start_lng = locations[0]["lng"]
            zoom = 10
        folium_map = folium.Map(location=[start_lat, start_lng], zoom_start=zoom, attr_control=False, tiles="OpenStreetMap")
        if len(locations) > 1:
            bounds = [[loc['lat'], loc['lng']] for loc in locations]
            folium_map.fit_bounds(bounds, padding=(30, 30))

        marker_data = []

        for loc in locations:
            marker = folium.Marker(location=[loc['lat'], loc['lng']], popup=f"<b>{loc['name']}</b>", tooltip=loc['name'])
            marker.options['location_id'] = int(loc['id'])
            marker.add_to(folium_map)
            folium_map.get_root().script.add_child(folium.Element(f"window.{marker.get_name()} = {marker.get_name()};"))

            marker_data.append({
                "var_name": marker.get_name(),
                "id": int(loc['id'])
            })

        macro_root = folium_map.get_root().header
        hide_css = "<style>.leaflet-control-attribution {display: none !important; }</style>"
        macro_root.add_child(folium.Element(hide_css))

        marker_data_json = json.dumps(marker_data)

        click_script = """
                        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
                        <script>
                            var bridge;
                            var markerData = __MARKER_DATA__;
                            new QWebChannel(qt.webChannelTransport, function (channel) {
                                bridge = channel.objects.pyBridge;
                            });

                            function onMapClick(e) {
                                if (bridge) {
                                    bridge.receive_coords(e.latlng.lat, e.latlng.lng);
                                }
                            }

                            document.addEventListener('contextmenu', function(e) { e.preventDefault(); });

                            setTimeout(function() {
                                var map_elements = document.getElementsByClassName('folium-map');
                                if (map_elements.length > 0) {
                                    var map_id = map_elements[0].id;
                                    var mapObject = window[map_id];
                                    if (mapObject) {
                                        mapObject.on('click', onMapClick);

                                        markerData.forEach(function(item) {
                                            var markerObject = window[item.var_name];
                                            if (markerObject) {
                                                markerObject.on('contextmenu', function(e) {
                                                    if (e.originalEvent) {
                                                        e.originalEvent.preventDefault();
                                                        e.originalEvent.stopPropagation();
                                                    }
                                                    if (bridge) {
                                                        bridge.receive_marker_id(item.id);
                                                    }
                                                });
                                            }
                                        });
                                    }
                                }
                            }, 300);
                        </script>
                        """

        click_script = click_script.replace("__MARKER_DATA__", marker_data_json)
        folium_map.get_root().html.add_child(folium.Element(click_script))

        html_data = folium_map.get_root().render()
        self.browser.setHtml(html_data)
