from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PredictForm
from django.contrib.auth.decorators import login_required
# added
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_for_files = os.path.join(base_dir, 'staticfiles/')

ALGORITM_LINK = "http://127.0.0.1:8000/api/v1/income_classifier/predict?parent_mlalgorithm=8&version=1.1.1"

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'your count has been created  {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def preprocessing_befor_load(df):
    # convert dates
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['year'] = df['Date'].dt.year.astype('uint16')
    df['month'] = df['Date'].dt.month.astype('uint8')
    df['season'] = df['month'].apply(lambda x: 1 if x in [1,11,12] else
                                    2 if x in [3, 4, 5] else
                                    3 if x in [6, 7, 8] else 4).astype('uint8')
    # replace wind directions with numeric
    wind_rose = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    dict_replacer = dict(zip(wind_rose, range(len(wind_rose))))
    df.replace(dict_replacer, inplace=True)
    # drop
    df.drop(['Date'], axis=1, inplace=True)
    return df

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        context = {'u_form': u_form, 'p_form': p_form}
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f' account has been updated')
            return redirect('profile') # update the form without reloading
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)

# @login_required
def predict_func(request):
    data = {}
    if "GET" == request.method:
        return render(request, "users/predict.html", data)

    if "POST" == request.method:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, f'File is not CSV type')
            return HttpResponseRedirect(reverse("predict"))

        file_data = pd.read_csv(csv_file)
        file_data = preprocessing_befor_load(file_data)
        data_dict = file_data.to_dict('records')
        location_dict = pd.read_csv(root_for_files + 'pred_graph.csv')

        location_id = []
        probability = []
        for i in range(len(data_dict)):
            r = requests.post(ALGORITM_LINK, data_dict[i])
            response = r.json()
            # get location ID
            location = data_dict[i]['Location_ID']
            probability.append(response['probability'])
            location_id.append(data_dict[i]['Location_ID'])
            messages.success(request, f'location is {location} weather is {response}')
        # # Graph
        temp = pd.DataFrame(zip(location_id, probability), columns=['Location_ID', 'probability'])
        temp = pd.merge(temp, location_dict, how='left', on='Location_ID')
        temp.to_csv(root_for_files + 'temp.csv', index=False)

    return render(request, 'users/predict.html', context={'temp':temp})

def predict_text(request):

    te = {"Location_ID": 3, "Cloud9am": 3.7053842498945335, "Cloud3pm": 3.7237069359428685, "Humidity9am": 35.0, "Humidity3pm": 33.0, "Pressure9am": 1012.2, "Pressure3pm": 1009.5, "MinTemp": 23.5, "MaxTemp": 35.8, "Temp9am": 29.7, "Temp3pm": 34.9, "Rainfall": 0.0, "Evaporation": 9.622704697893075, "Sunshine": 9.213206202001825, "WindGustDir": 5, "WindGustSpeed": 50.0, "WindDir9am": 2, "WindDir3pm": 4, "WindSpeed9am": 6.0, "WindSpeed3pm": 9.0, "year": 2017, "month": 1, "season": 1}

    responce_json = {}

    if 'POST' == request.method:
        json_data = request.POST
        temp_request = json_data['json_text']
        r_json = requests.post(ALGORITM_LINK, te)
        responce_json = r_json.json()
        messages.success(request, f'we predict rain with {responce_json}')

    return render(request, 'users/predict_text.html', context={'responce_json':responce_json, 'te':te})
