from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests

# Create your views here.

def all_weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=YOUR_KEY'

    err_msg=""
    message=""
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data["name"]
            existing_citycount=City.objects.filter(name=new_city).count()
            
            if existing_citycount ==0:
                r=requests.get(url.format(new_city)).json()
                if r["cod"]==200:
                    form.save()
                else:
                    err_msg="City Does Not Exist."
            else:
                err_msg="City Already Exists!"


        if err_msg:
            message=err_msg
        
        else:
            message="City Added Succesfully!"  
           


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

    
    
    context={'weather_data':weatherdata,'form':form,'message':message}
    return render(request,'weather_app/home.html',context=context)
