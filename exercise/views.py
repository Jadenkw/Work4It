from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views import View
from .models import Workout
from .models import Item
from .forms import WorkoutForm
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
import operator


def index(request):
    return render(request, 'exercise/index.html')

def video(request):
    obj = Item.objects.all()
    return render(request, 'exercise/video.html', {'obj': obj})

def addWorkout(request):
    render(request, 'exercise/workout.html')
    #context = {}
    if request.method == 'POST':
        #form = WorkoutForm(request.POST)
        #if form.is_valid():
        workout=Workout()
        workout.user = request.user
        workout.workout_title= request.POST.get('workout_title')
        workout.workout_pub_date= request.POST.get('workout_pub_date')
        workout.workout_start_time = request.POST.get('workout_start_time')
        workout.workout_end_time = request.POST.get('workout_end_time')
        workout.workout_description = request.POST.get('workout_description')
        workout.workout_calories = request.POST.get('workout_calories')
        '''
        I know this way of calculating points is super wack, but honestly I was trying for
        3 hours to convert this into a form and nothing was working, so this should be good for now
        '''
        starttime = int((str(workout.workout_start_time))[0:2] + (str(workout.workout_start_time))[3:5])
        endtime = int((str(workout.workout_end_time))[0:2] + (str(workout.workout_end_time))[3:5])
        if(endtime < starttime):
            workout.workout_points = int((starttime-endtime) * (0.01 * int(workout.workout_calories)))
        elif(endtime > starttime):
            workout.workout_points = int((endtime-starttime) * (0.01 * int(workout.workout_calories)))
        else:
            workout.workout_points = 0 # they worked out for a full day??
        workout_dict = Workout.objects.filter(user=request.user)
        totalpoints = 0
        for w in workout_dict:
            totalpoints += w.workout_points
        level = calcLevel(totalpoints)
        workout.save()
        return redirect('exercise:dashboard')
    return render(request, 'exercise/workout.html')

def dashboardView(request):
    render(request, 'exercise/index.html')
    workout_dict = Workout.objects.filter(user=request.user)
    totalpoints = 0
    for w in workout_dict:
        totalpoints += w.workout_points
    level = calcLevel(totalpoints)
    for x in workout_dict:
        temp = x.workout_pub_date
        date = temp.strftime("%B %d, %Y")       # FOR TABLE OF WORKOUTS
        x.workout_pub_date = date
    
    date_calories_query = Workout.objects.filter(user=request.user) # FOR GOOGLE CHARTS API
    date_calories = dict()
    for y in date_calories_query:
        temp = y.workout_pub_date
        # print(temp)
        year = temp.strftime("%Y")
        month = temp.strftime("%m")
        day = temp.strftime("%d")
        calories = y.workout_calories
        date_calories[y.workout_title] = [int(year), int(month)-1, int(day), int(calories)]
    #print(date_calories)
    pointstonext = toNextLevel(totalpoints)
    return render(request, 'exercise/dashboard.html', {'workout_dict': workout_dict, 'date_calories': date_calories, 'totalpoints':totalpoints, 'level':level, 'pointstonext':pointstonext})

def leaderboardView(request):
    render(request, 'exercise/index.html')
    all_users = User.objects.all()
    leaderboard = {}
    totalpoints = 0
    userrank = 0
    for currentuser in all_users: # loop through all users
        userworkouts = Workout.objects.filter(user=currentuser) # grab all workouts for current user
        for workout in userworkouts: # for all currentuser's workouts
            totalpoints += workout.workout_points # add points to totalpoints
        leaderboard[currentuser.username] = totalpoints
        totalpoints = 0

    sortedboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True) # sort the leaderboard by descending total points
    outsideoften = False
    for i in range(0,len(sortedboard)):
        if(sortedboard[i][0] == request.user.username):
            userrank = i+1
    if(userrank > 10):
        outsideoften = True
    print(userrank)
    if(request.user.is_authenticated):
        workout_dict = Workout.objects.filter(user=request.user)
        totalpoints = 0
        for w in workout_dict:
            totalpoints += w.workout_points
    level = calcLevel(totalpoints)
    pointstonext = toNextLevel(totalpoints)
    return render(request, 'exercise/leaderboard.html', {'leaderboard':sortedboard[0:10], 'totalpoints':totalpoints, 'level':level, 'pointstonext':pointstonext, 'userrank':userrank, 'outsideten':outsideoften})

def calcLevel(points): # calculate the user's level based on increments of 500 points
    if(points == 0):
        return 1
    level = 0
    while(points > 0):
        points -= 1000
        level+=1
    return level

def toNextLevel(points): # calculates the points needed to next level
    next = 0
    while(next < points):
        next += 1000
    return abs(next-points)



