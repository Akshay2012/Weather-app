from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests

# Create your views here.

def all_weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0ab9856cd9a03044b1bdb1530ab6755e'

    err_msg=""
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data["name"]
            existing_citycount=City.objects.filter(name=new_city).count()
            
            if existing_citycount ==0:
                form.save()
            else:
                err_msg="City Already Exists!"
                
    form = CityForm()

    cities= City.objects.all()

    weatherdata=[]

    for city in cities:

        r=requests.get(url.format(city)).json()
        #print(r)
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weatherdata.append(city_weather)

    
    
    context={'weather_data':weatherdata,'form':form}
    return render(request,'weather_app/home.html',context=context)