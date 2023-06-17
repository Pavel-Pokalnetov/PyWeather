from modules import weather
from modules import emailer

if __name__=="__main__":
    api_key = "<you_api_key>"
    city = "Салехард"
    html_page = weather.get_weather_html(city, api_key)
    #print(html_page)
    emailer.send_email(html_page,'modules\\recipients.csv')