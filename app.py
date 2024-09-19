from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        api_key = "be0e368abd51d75e834d552ac8310f7f"  
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        data = response.json()
        
        if data["cod"] != "404":
            weather = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "visibility": data["visibility"],
                "icon": data["weather"][0]["icon"]
            }
        else:
            weather = "City not found!"
    return render_template("index.html", weather=weather)

@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    forecast_data = None
    if request.method == "POST":
        city = request.form.get("city")
        api_key = "be0e368abd51d75e834d552ac8310f7f"  
        base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        data = response.json()
        
        if data["cod"] != "404":
            forecast_data = []
            for item in data["list"]:
                forecast_data.append({
                    "date": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"]
                })
        else:
            forecast_data = "City not found!"
    return render_template("forecast.html", forecast=forecast_data)

if __name__ == "__main__":
    app.run(debug=True)
