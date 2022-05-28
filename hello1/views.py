from web_project1.settings import MODEL_URL
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
import pymysql.cursors
import hello1.connections
from django.core.files.storage import FileSystemStorage

from imutils import is_cv2
import numpy as np
import cv2
import skimage.measure
import matplotlib.pyplot as plt
from PIL import Image


from hello1.find_green_area import area_find
from hello1.plot_chart import plot_pie

from hello1.models import User

from matplotlib.pyplot import figure

from django.http import HttpResponse

# import hello1.image_algo as image_algo
from hello1.image_algo import image_process

import urllib
import base64
import pandas as pd
import io
from io import BytesIO
from io import StringIO
import matplotlib.pyplot as plt
import urllib.request

import os
import glob

import ee

import random 


import base64

# matplot

# from matplotlib import pylab
# from pylab import *
# import PIL, PIL.Image, StringIO

# import matplotlib.pyplot as plt

# from matplotlib.pyplot import grid
# import math
# from math import cos
# from math import pi

# import numpy as np
# import io


# darshitrawal0703@gmail.com
# Darshit@123


# def getimage(request):
#     # Construct the graph
#     x = np.arange(0, 2*pi, 0.01)
#     s = cos(x)**2
#     plt.plot(x, s)     
#     plt.xlabel('xlabel(X)')
#     plt.ylabel('ylabel(Y)')
#     plt.title('Simple Graph!')
#     grid(True)
#     # Store image in a string buffer
#     buffer = io.StringIO()
#     canvas = pylab.get_current_fig_manager().canvas
#     canvas.draw()
#     pilImage = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
#     pilImage.save(buffer, "PNG")
#     pylab.close()
#     # Send buffer in a http response the the browser with the mime type image/png set
#     return HttpResponse(buffer.getvalue(), mimetype="image/png")
#     convert graph into dtring buffer and then we convert 64 bit code into image

def dashboard(request):
    return render(request, 'dashboard.html', {'result': True})


def css(request):
    return render(request, 'imageupload_copy.html')


def earthengine(request):
    return render(request, 'earthengineImage.html')


def forestApproximation(request):
    return render(request, 'ForestApproximation.html')


def forestfire(request):
    return render(request, 'forestfire.html')


def postforestfire(request):
    months = ['feb','mar','apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    days = ['tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    if request.method == 'POST':
        x = request.POST.get('x')
        y = request.POST.get('y')
        month = request.POST.get('month')
        day = request.POST.get('day')
        FFMC = request.POST.get('FFMC')
        DMC = request.POST.get('DMC')
        DC = request.POST.get('DC')
        ISI = request.POST.get('ISI')
        temp = request.POST.get('temp')
        RH = request.POST.get('RH')
        wind = request.POST.get('wind')
        rain = request.POST.get('rain')
        dataframe_data = [{'x': x, 'y': y, 'month': month, 'day': day, 'FFMC': FFMC,
                          'DMC': DMC, 'DC': DC, 'ISI': ISI, 'temp': temp, 'RH': RH, 'wind': wind, 'rain': rain}]

        df = pd.DataFrame(dataframe_data)
        for month in months:
            df.insert(len(df.columns), month, 0,True)    
        for day in days:
            df.insert(len(df.columns), day, 0,True)
        if df['month'][0] != 'jan':
            df[df['month'][0]][0] = 1
        if df['day'][0] != 'mon':
            df[df['day'][0]][0] = 1
        df = df.drop(columns=['month','day'])  
        data = df.values
        path = MODEL_URL
        mx_scaler = pd.read_pickle(path + "scaler.pickle")
        data_trans = mx_scaler.transform(data)
        regressor = pd.read_pickle(path + "regressor_forest.pickle")
        data_test = regressor.predict(data_trans)
        prediction = data_test
        return render(request, "postforestfire.html", {'prediction': prediction})


def error_404_view(request, exception):
    return render(request, '404page.html')


def login(request):
    user = User()
    user.password = ""
    user.email = ""
    messages.success(request, "")
    return render(request, 'login.html', {'user': user})


def loginDatabase(request):
    connection = hello1.connections.getConnection()
    sql = "Select * from user "
    cursor = connection.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    return render(request, "userdata.html", {'users': users})
    # username = request.POST["username"]
    # user = User.objects.all()
    # return render(request, "userdata.html", {'user':user})


def register(request):
    return render(request, 'register.html')


def visulizeForest(request):
    return render(request, 'visulize.html')


def postlogin(request):
    connection = hello1.connections.getConnection()
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        sql = "Select * from user where email = %s and password = %s"
        cursor = connection.cursor()
        row = cursor.execute(sql, (email, password))
        if row > 0:
            # messages.success(request, "successful")
            return render(request, 'dashboard.html')
        else:
            # messages.success(request, "Invalid credential!!!")
            return render(request, 'login.html')

        # try:
        #     user = User.objects.get(email=email, password=password)
        #     messages.success(request, "successful")
        #     return render(request, 'dashboard.html')
        # except:
        #     messages.success(request, "Invalid credential!!!")
        #     return render(request, 'login.html')

        # # if user != None:
        #     messages.success(request, "successful")
        #     return render(request, 'register.html')
        # # else:
        # #     messages.success(request, "sorry")
        # #     return render(request, 'login.html')


def postRegistration(request):
    if request.method == 'POST':
        newUser = User()
        newUser.name = request.POST.get('name')
        newUser.password = request.POST.get('password')
        newUser.email = request.POST.get('email')
        newUser.userType = request.POST.get('userType')
        newUser.organizationName = request.POST.get('organizationName')
        connection = hello1.connections.getConnection()
        sql = "INSERT INTO `user` (`name`, `password`, `email`, `userType`, `organizationName`) VALUES (%s, %s, %s, %s, %s)"
        cursor = connection.cursor()
        cursor.execute(sql, (newUser.name, newUser.password,
                             newUser.email, newUser.userType, newUser.organizationName))
        connection.commit()
        return render(request, 'login.html')
    else:
        # messages.success(request, "sorry")
        return render(request, 'register.html')
    #     newUser.save()
    #     return render(request, 'login.html')
    # else:
    #     messages.success(request, "sorry")
    #     return render(request, 'register.html')


def home(request):
    plt.plot(range(10))
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'home.html', {'data': uri})


def upload(request):
    connection = hello1.connections.getConnection()
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        sql = "INSERT INTO `imagetable` (`path`) VALUES (%s)"
        cursor = connection.cursor()
        print(context)
        cursor.execute(sql, (context['url']))
        connection.commit()
        sql = "Select * from imagetable "
        cursor = connection.cursor()
        url = cursor.execute(sql)
        print(url)
    return render(request, 'imageupload.html', context)

    
def postdashboard(request):
    connection = hello1.connections.getConnection()
    context = {}
    if request.method == 'POST':
        uploaded_file1 = request.FILES['file1']
        uploaded_file2 = request.FILES['file2']

        fs = FileSystemStorage()
        name1 = fs.save(uploaded_file1.name, uploaded_file1)
        name2 = fs.save(uploaded_file2.name, uploaded_file2)
        context['url1'] = fs.url(name1)
        context['url2'] = fs.url(name2)
        path1 = '.' + context['url1']
        path2 = '.' + context['url2']
        sql = "INSERT INTO `imagetable` (`path1`, `path2`) VALUES (%s, %s)"
        cursor = connection.cursor()
        cursor.execute(sql, (context['url1'], context['url2']))
        connection.commit()

        url1, url2, url3, uri, per = image_process(path1, path2)

        charts = {}
        charts['original'] = url1
        charts['modified'] = url2
        charts['difference'] = url3
        charts['figure'] = uri

        return render(request, 'getimage.html', {'url': charts})


def getimage(request):
    connection = hello1.connections.getConnection()
    sql = "Select * from imagetable "
    cursor = connection.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    print(users)
    return render(request, "getimage.html", {'users': users})


def postearthengine(request):
    choice = request.POST.get('submit')
    date_arg1 = request.POST.get('date1')
    date_arg2 = request.POST.get('date2')
    latitude = float(request.POST.get('latitude'))
    longitude = float(request.POST.get('longitude'))
    ee.Initialize()
    tempDec = ee.ImageCollection('MODIS/006/MOD13A2')

    center = [longitude, latitude]  # 70.610, 21.167
    point1 = center[0] - 1
    point2 = center[1] + 1
    point3 = center[0] + 1
    point4 = center[1] - 1

    aoi = ee.Geometry.Rectangle([point1, point2, point3, point4])

    videoArgs = {
        'dimensions': 768,
        'region': aoi,
        'framesPerSecond': 2,
        'crs': 'EPSG:3857',
        'palette': ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901', '66A000', '529400', '3E8601',
                    '207401', '056201', '004C00', '023B01', '012E01', '011D01', '011301'],
        'min': 0.0,
        'max': 9000.0,
    }

    print(choice)
    if choice == "Analyze":
        connection = hello1.connections.getConnection()
        context = {}

        if request.method == 'POST':
            years = []
            year1 = date_arg1.split("-")
            year2 = date_arg2.split("-")
            # years.append(request.POST.get('year1'))
            # years.append(request.POST.get('year2'))

            for i in range(int(year1[0]), int(year2[0])):
                years.append(str(i))

            years.append(str(year2[0]))

            print(years)

            images = {}
            i = 0
            for year in years:
                date1 = year + "-" + year1[1] + "-01"
                date2 = year + "-" + year2[1] + "-15"
                tempCol = tempDec.filterDate(
                    date1, date2).limit(24).select('NDVI')
                url1 = tempCol.getVideoThumbURL(videoArgs)
                image1 = Image.open(urllib.request.urlopen(url1))
                i += 1
                url2 = "./Temp/image" + str(i) + ".png"
                image1.save(url2)

                index = "image" + str(i)
                images[index] = url2

            val_year = []
            val_diff = []
            charts = {}
            j = 0
            for j in range(1, len(years)):
                url1, url2, url3, uri, diff_per = image_process(
                    images['image' + str(j)], images['image'+str(j+1)])
                
                charts['original'] = url1
                charts['modified'] = url2
                charts['difference'] = url3
                charts['figure'] = uri
                charts['diff'] = diff_per
                # print(images['image1'])
                # print("---------------------")
                # print(images['image2'])
                # print("----------------------")
                # print(diff_per)
                val_year.append(str(years[j-1])+"-"+str(years[j]))
                val_diff.append(charts['diff'])

            # print("------------------------- val_year ---------------------------------")
            # print(val_year)
            # print(val_diff)

            figure(num=None, figsize=(8, 6), dpi=90,
                   facecolor='w', edgecolor='k')
            plt.bar(val_year, val_diff)
            plt.xlabel("Years")
            plt.xticks(rotation=40)
            plt.ylabel("Forest Difference (in %)")
            plt.title("Forest Analysis")
            # plt.show()

            print(j)

            path1 = "./Temp/image1.png"
            path2 = "./Temp/image" + str(j + 1) + ".png"
            green_area = []
            green_area.append(round(area_find(path1), 2))
            green_area.append(round(area_find(path2), 2))
            print(green_area)
            fig1 = plt.gcf()
            buf = io.BytesIO()
            fig1.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            urx = urllib.parse.quote(string)
            charts['bar'] = urx

            # pie chart

            lable = [years[0], years[len(years) - 1]]
            ury = plot_pie(lable, green_area)
            charts['pie'] = ury
            plt.clf()
            files = glob.glob('./Temp/*')
            for f in files:
                os.remove(f)
            return render(request, 'getEarthImage.html', {'url': charts})
    else:
        import string
        imageUrl = {}
        size = 7
        earth_eninge_call = tempDec.filterDate(date_arg1, date_arg2).limit(24).select('NDVI')
        url_pass = earth_eninge_call.getVideoThumbURL(videoArgs)
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = size))
        path_pass = "./media/"+str(res)+".gif"
        urllib.request.urlretrieve(url_pass, path_pass)
        imageUrl['urz'] = path_pass
        return render(request, 'visulize.html', {'url': imageUrl})
