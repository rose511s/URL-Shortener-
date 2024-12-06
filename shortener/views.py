from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import LongToShort

from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.express as px
import pandas as pd


def example_view(request, name):
    # name slug variable
    data = {
        'name': name
    }
    return render(request, 'index.html', data)
# Create your views here.


def task_view(request):
    data = {
        'task': 'django workshop'
    }
    return render(request, 'task.html', data)


def shorten_url(request):
    context = {
        "submitted": False,
        "error": False
    }
    if request.method == "POST":
        context['submitted'] = True
        user_data = request.POST

        long_url = user_data['longurl']
        custom_name = user_data['custom_name']
        data = {}
        data['long_url'] = long_url
        data['short_url'] = request.build_absolute_uri() + custom_name
        try:
            obj = LongToShort(long_url=long_url, short_url=custom_name)
            obj.save()

            date = obj.date
            clicks = obj.clicks
            data['date'] = date
            data['clicks'] = clicks
            context['data'] = data
        except:
            context['submitted'] = False
            context['error'] = True

    return render(request, 'home.html', context)


def redirect_url(request, shorturl):
    if request.user.is_anonymous:
        redirect('Login')
    row = LongToShort.objects.filter(short_url=shorturl)
    if len(row) == 0:
        return render(request, 'error.html')
    obj = row[0]
    long_url = obj.long_url
    obj.clicks += 1
    analytics = request.headers['user-agent']
    if "OPR" in analytics or "Opera" in analytics:
        obj.opera += 1
    elif "Firefox" in analytics:
        obj.firefox += 1
    elif "Chrome" in analytics:
        obj.chrome += 1
    else:
        obj.others += 1

    if request.META['HTTP_SEC_CH_UA_MOBILE'] == '?0':
        obj.desktop += 1
    else:
        obj.mobile += 1
    obj.save()
    return redirect(long_url)


def all_analytics(request):
    if request.user.is_anonymous:
        redirect('Login')
    rows = LongToShort.objects.all()
    context = {
        "rows": rows
    }
    print(rows)
    return render(request, 'all_analytics.html', context)


def analytics(request, short_url):
    if request.user.is_anonymous:
        redirect('Login')
    row = LongToShort.objects.filter(short_url=short_url)
    if len(row) == 0:
        return render(request, 'error.html')
    obj = row[0]
    data = [['opera', obj.opera], ['Chrome', obj.chrome],
            ['Firefox', obj.firefox], ['others', obj.others]]
    df = pd.DataFrame(data=data, columns=['Browser', 'Number of Accesses'])
    plot_div = plot(px.pie(df, values='Number of Accesses', names='Browser',
                    title='Browser Accessing the link'), output_type='div')
    context = {'plot_div_1': plot_div}
    data = [['desktop', obj.desktop], ['mobile', obj.mobile]]
    df = pd.DataFrame(data=data, columns=['Device', 'Count'])
    plot_div = plot(px.bar(df, x='Device', y='Count', color='Device',
                    title='Devices Used'), output_type='div')
    context['plot_div_2'] = plot_div
    context['long_url'] = obj.long_url
    context['date'] = obj.date
    context['short_url'] = obj.short_url
    context['clicks'] = obj.clicks
    return render(request, "analytics.html", context)
    # data = [
    #     ['Year', 'Sales', 'Expenses'],
    #     [2004, 1000, 400],
    #     [2005, 1170, 460],
    #     [2006, 660, 1120],
    #     [2007, 1030, 540]
    # ]
    # DataSource object
    # data_source = SimpleDataSource(data=data)
    # # Chart object
    # chart = LineChart(data_source)
    # context = {'chart': chart}
    # return render(request, 'analytics.html', context)


def loginFunc(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'You have successfully logged in')
            return redirect('Home')
        else:
            return redirect('Login')
    return render(request, 'loginPage.html')


def registerFunc(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        # print(username, email, firstname, lastname, password)
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'You have successfully logged in')
            return redirect('Home')
        else:
            return redirect('Login')
    return render(request, 'register.html')


def logoutFunc(request):
    logout(request)
    return redirect('Home')