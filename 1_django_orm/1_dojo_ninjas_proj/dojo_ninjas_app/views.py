from django.shortcuts import render, redirect
from .models import Dojos, Ninjas


def index(request):
    context = {
        "dojos_objects": Dojos.objects.all(),
    }
    return render(request, "index.html", context)


def create_dojo(request):
    Dojos.objects.create(
        name=request.POST['name'],
        city=request.POST['city'],
        state=request.POST['state'],
    )
    return redirect("/")


def create_ninja(request):
    Ninjas.objects.create(
        fname=request.POST['fname'],
        lname=request.POST['lname'],
        # request.POST['dojo'] asks specifically for the id of the dojo you're diggin in currently
        dojo=Dojos.objects.get(id=request.POST['dojo']),
    )
    return redirect("/")

# Work In Progress
# def delete_dojo(request):
#     Dojos.objects.get(request.POST['delete'])
#     return redirect("/")
