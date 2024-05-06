import csv
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.db import IntegrityError
from .models import User,Task,Remark,Reminder
from django.core.paginator import Paginator

def index(request):
    if request.user.is_authenticated:
        current_tasks=list(Task.objects.filter(user=request.user,end_time=None).values())
        completed_tasks=list(Task.objects.filter(user=request.user, end_time__isnull=False).values())
        reminders=list(Reminder.objects.filter(user=request.user).values())
        for task in current_tasks:
            myvar=timezone.now()-task["start_time"]
            task["duration"]=f"{round(myvar.seconds//3600)}hrs {(myvar.seconds//60)%60}min"
        for task in completed_tasks:
            myvar=task["end_time"]-task["start_time"]
            task["duration"]=f"{round(myvar.seconds//3600)}hrs {(myvar.seconds//60)%60}min"
            task["remark"]=Remark.objects.get(task_id=task["id"]).remark
        groups=[]
        for i in Task.objects.filter(user=request.user).values():
            groups += [i["group"]]
        grouptags=set(groups)
        reminders.reverse()
        completed_tasks.reverse()
        try:
            pageno=request.POST["page"]
        except:
            pageno="1"
        page_obj=Paginator(completed_tasks, 10)
        
        return render(request, "proList/index.html", {
            "current_tasks":current_tasks,
            "completed_tasks":page_obj.page(pageno),
            "reminders":reminders,
            "groups":grouptags,
            "page_obj":page_obj,
            "curr_page":pageno,
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            print("Logged in")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "proList/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "proList/login.html", {
            "message": "Please login to continue"
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "proList/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "proList/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "proList/register.html")

@login_required
def newtask(request):
    if request.method == "POST":
        taskname=request.POST['task']
        taskgroup=request.POST['group']
        newtask=Task(user=request.user, task=taskname,start_time=timezone.now(),group=taskgroup)
        newtask.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def endtask(request):
    if request.method == "POST":
        taskid=request.POST["task_id"]
        remark_content=request.POST["remark"]
        task=Task.objects.get(id=taskid)
        task.end_time=timezone.now()
        task.save()
        remark=Remark(task=task,remark=remark_content)
        remark.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def addreminder(request):
    if request.method == "POST":
        reminder=request.POST["new_reminder"]
        newreminder=Reminder(user=request.user,reminder=reminder)
        newreminder.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def endreminder(request):
    if request.method=="POST":
        toend=request.POST["reminder_id"]
        Reminder.objects.get(id=toend).delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def taskgroup(request):
    if request.method == "POST":
        group=request.POST["groupname"]
        if group == "ALL":
            tasks=list(Task.objects.filter(user=request.user, end_time__isnull=False).values())
        else:
            tasks=list(Task.objects.filter(user=request.user, group=group, end_time__isnull=False).values())
        for task in tasks:
            myvar=task["end_time"]-task["start_time"]
            task["duration"]=f"{round(myvar.seconds//3600)}hrs {(myvar.seconds//60)%60}min"
            task["remark"]=Remark.objects.get(task_id=task["id"]).remark
            task['start_time'] = task['start_time'].strftime("%B %d, %Y, %I:%M %p")
            task['end_time'] = task['end_time'].strftime("%B %d, %Y, %I:%M %p")
        tasks.reverse()
        return JsonResponse({
            "tasks":tasks
        })
    
@login_required
def export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    if request.method == "POST":
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="data.csv"'},
        )
        writer = csv.writer(response)
        group=request.POST['groupname']
        if group=="ALL":
            tasks = list(Task.objects.filter(user=request.user, end_time__isnull=False).values())
        else:
            tasks = list(Task.objects.filter(user=request.user, end_time__isnull=False, group=group).values())
        exportdata=[]
        for task in tasks:
            myvar=task["end_time"]-task["start_time"]
            duration=f"{round(myvar.seconds//3600)}hrs {(myvar.seconds//60)%60}min"
            remark = Remark.objects.get(task_id=task['id'])
            exportdata += [[task['task'], task['start_time'].strftime("%m/%d/%Y, %H:%M:%S"), task['end_time'].strftime("%m/%d/%Y, %H:%M:%S"), duration,
                            task['group'], remark.remark]]
        exportdata.reverse()
        writer.writerow(["Task", "Start time (mm/dd/yyyy)", "End Time (mm/dd/yyyy)", "Duration","Group", "Remark"])
        for data in exportdata:
            writer.writerow(data)
        return response
    return HttpResponseRedirect(reverse('index'))