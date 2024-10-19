from flask import Flask, render_template, render_template_string, request, jsonify
from geopy.geocoders import Nominatim
import folium

app = Flask(__name__)

@app.route('/')
def main_app():
    return render_template('index.html')

@app.route('/firstresponse')
def firstresponse():
    return render_template('firstresponse.html')

@app.route('/map', methods=('GET', 'POST'))
def mapping():
    global allWarnings
    allWarnings = ""

    geolocator = Nominatim(user_agent="location_finder")

    soFloMap = folium.Map(location=(26.927918, -81.326507), zoom_start=7)

    storage = open("storage.txt", "r")
    listStorage = storage.readlines()
    storage.close()

    print(listStorage)

    if request.method == "POST":
       items = request.form.get("items")
       locart = request.form.get("locart")
       locator = request.form.get("fname")

       if ((items != None) and (locart != None)):
        storage = open("storage.txt", "a")
        if ((items + " / " + locart) not in listStorage):
            storage.write("\n" + items + " / " + locart)
        storage.close()

       if (locator != None):
        query = "gas stations near " + locator
        locations = geolocator.geocode(query, exactly_one=False, limit=10)

        if locations:
            for location in locations:
                allWarnings += "<br>" + location.address
                for line in listStorage:
                    if ((line[:line.find("/")-1] in location.address) and (line.find("/") > -1) ):
                        allWarnings += (" | Shortage of: " + line[line.find("/") + 2:])
                folium.Marker(location=[location.latitude,location.longitude], popup=location.address).add_to(soFloMap)
        else:
            print("No " + query + ".")

    else:
       query = "."

    soFloMap.get_root().width = "800px"
    soFloMap.get_root().height = "600px"
    iframe = soFloMap.get_root()._repr_html_()

    return render_template('map.html', iframe=iframe, allWarnings = allWarnings,
    )

if __name__ == '__main__':
    app.run(debug=True)
    
