from qgis.core import *
import json

layer = QgsProject.instance().mapLayersByName("BPE_CA_PB_skatepark")[0]
parameter = {
    'INPUT': layer,
    'TARGET_CRS': 'EPSG:4326',
    'OUTPUT': 'memory:Reprojected'
}
result_reproj = processing.run('native:reprojectlayer', parameter)['OUTPUT']

result_list = []

for f in result_reproj.getFeatures():
    geom = f.geometry()
    pt = geom.asPoint()
    result_list.append({
        "lon": pt.x(),
        "lat": pt.y(),
    })

print(json.dumps(result_list))
