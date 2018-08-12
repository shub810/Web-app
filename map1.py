import folium
import pandas

def colorProducer(el):
    if el < 1000:
        return 'green'
    elif 1000 <= el < 3000:
        return 'orange'
    else:
        return 'red'


dfv = pandas.read_csv("Volcanoes_USA.txt")
lat = list(dfv.LAT)
lng = list(dfv.LON)
elev = list(dfv.ELEV)
vName = list(dfv.NAME)

map = folium.Map(location=[38.58, -90.09], zoom_start=6, tiles="MapBox Bright")
fgvc = folium.FeatureGroup(name="Volcanoes circle marker")
fgvm = folium.FeatureGroup(name="Volcanoes marker")

for lt, lng, el, name in zip(lat, lng, elev, vName):
    # fg.add_child(folium.Marker(location=[lt, lng], popup=str(el) + " m", icon=folium.Icon(color=colorProducer(el))))
    fgvm.add_child(folium.Marker(location=[lt, lng], popup=folium.Popup(name, parse_html=True), icon=folium.Icon(color='green')))
    fgvc.add_child(folium.CircleMarker(
        location=[lt, lng],
        radius=6,
        popup=str(el) + " m",
        color='grey',
        fill=True,
        fill_color=colorProducer(el),
        fill_opacity=0.7
        ))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson((open("world.json", encoding = "utf-8-sig")).read(),
    style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' }
))

map.add_child(fgvm)
map.add_child(fgvc)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
