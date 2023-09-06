from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
import datetime
import re

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from django.http import JsonResponse
import json

from .models import User, Customer, Task

# Create your views here.

# Dashboard
def index(request):

    # Render Dashboard if user is authenticated
    if request.user.is_authenticated:

        # Get all tasks from the current user with finish date today
        today_tasks = Task.objects.all().filter(task_to_user=request.user, task_date=datetime.datetime.today(), task_done=False)

        # Count all today finish tasks
        today_tasks_count = 0

        for _ in today_tasks:
            today_tasks_count += 1


        # Get all tasks from the current user which are open
        open_tasks = Task.objects.all().filter(task_to_user=request.user, task_done=False)

        # Count all open tasks
        open_tasks_count = 0

        for _ in open_tasks:
            open_tasks_count += 1


        # Get all tasks from the current user which are completed
        completed_tasks = Task.objects.all().filter(task_to_user=request.user, task_done=True)

        # Count all completed tasks
        completed_tasks_count = 0

        for _ in completed_tasks:
            completed_tasks_count += 1


        # Get all customers from the current user
        customer_objects = Customer.objects.all().filter(to_user=request.user)

        # Count all customers
        customers_count = 0

        for _ in customer_objects:
            customers_count += 1


        return render(request, "crm_system/index.html", {
            "today_tasks_count": today_tasks_count,
            "open_tasks_count": open_tasks_count,
            "completed_tasks_count": completed_tasks_count,
            "customers_count": customers_count
        })
    # Render login page if user is not authenticated
    else:
        return render(request, "crm_system/login.html")


# Handle the registration
def register_view(request):

    # Check if request method is post
    if request.method == "POST":
        username = request.POST["register-username"].strip()
        email = request.POST["register-email"].strip()
        password = request.POST["register-password"].strip()
        confirmation = request.POST["register-password-confirmation"].strip()

        # Check length of the username
        if len(username) < 5:
            return render(request, "crm_system/register.html", {
                "message": "Username must have five or more digits."
            })

        # Check length of the password
        if len(password) < 8:
            return render(request, "crm_system/register.html", {
                "message": "Password must have eight or more digits."
            })


        # Check email form
        email_form = r"(^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$)"

        if not re.match(email_form, email):
            return render(request, "crm_system/register.html", {
                "message": "Email is not in the right form."
            })


        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "crm_system/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create the new user
        try:
            # Save new user if all intern restrictions was passed
            user = User.objects.create_user(username, email, password)
            user.save()
        # Throw Error if username is already taken and render register page again
        except IntegrityError:
            return render(request, "crm_system/register.html", {
                "message": "Username already taken, please choose a other."
            })

        # Log in user
        login(request, user)
        # Render Dashboard with the logged in user
        return HttpResponseRedirect(reverse("index"))

    # Render the register page if the method is get
    else:
        return render(request, "crm_system/register.html")


# Handle the Login
def login_view(request):

    # Post method attempt to log in unser
    if request.method == "POST":

        # Attempt to log in user
        username = request.POST["login-username"].strip()
        password = request.POST["login-password"].strip()
        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            # Log in the user and render Dashboard page
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # If log in was not successfully render login page again with a message
            return render(request, "crm_system/login.html", {
                "message": "Invalid username and/or password."
            })

    # Get method render the login page
    else:
        return render(request, "crm_system/login.html")


# Handle the Log out
def logout_view(request):
    # Log out the current user
    logout(request)

    # Redirect to the Log in page
    return HttpResponseRedirect(reverse("login_view"))


# Handle the customers function
@login_required(login_url='/crm_system/login.html')
def customers_view(request):

    if request.method == "POST":
        # Get new customers data from page
        first_name = request.POST["customer-firstname"].strip()
        last_name = request.POST["customer-lastname"].strip()
        email_address = request.POST["customer-email"].strip()

        # Check first name
        if len(first_name) < 2:
            return render(request, "crm_system/customers.html", {
                "message": "First name is to short."
            })
        elif len(first_name) > 50:
            return render(request, "crm_system/customers.html", {
                "message": "First name must be only 50 characters long."
            })

        # Check last name
        if len(last_name) < 2:
            return render(request, "crm_system/customers.html", {
                "message": "Last name is to short."
            })
        elif len(last_name) > 50:
            return render(request, "crm_system/customers.html", {
                "message": "Last name must be only 50 characters long."
            })

        # Check email form
        email_form = r"(^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$)"

        if not re.match(email_form, email_address):
            return render(request, "crm_system/customers.html", {
                "message": "Email is not in the right form."
            })

        # Calculate the id for the new customer of the authenticated user
        customer_count = Customer.objects.all().filter(to_user=request.user)
        customer_counter = 1
        for _ in customer_count:
            customer_counter += 1

        # Save new customer if all intern restrictions was passed
        new_customer = Customer(customer_id=customer_counter, first_name=first_name, last_name=last_name, email_address=email_address, info_box="Enter something...", to_user=request.user)
        new_customer.save()

        # Render Customers page
        return HttpResponseRedirect(reverse("customers_view"))
    elif "q" in request.GET:
        q = request.GET["q"]
        # Filter only searched first and last names
        data_filter = Q(Q(last_name__icontains=q) | Q(first_name__icontains=q))
        data = Customer.objects.filter(data_filter)
        # Filter customers for only the current user
        data = data.filter(to_user=request.user)

        # Pagination
        # Choose how much posts per page
        p = Paginator(data, 2)
        # Get the posts
        posts = p.get_page(request.GET.get('page'))

        return render(request, "crm_system/customers.html", {
            "page_obj": posts
        })
    else:
        # Get all customers for authenticated user in alphabetically order
        data = Customer.objects.all().filter(to_user=request.user).order_by("last_name")

        # Pagination
        # Choose how much posts per page
        p = Paginator(data, 4)
        # Get the posts
        posts = p.get_page(request.GET.get('page'))

        return render(request, "crm_system/customers.html", {
            "page_obj": posts
        })

# Handle the tasks function
@login_required(login_url='/crm_system/login.html')
def tasks_view(request):

    if request.method == "POST":
        # Get new tasks data from page
        task_name = request.POST["task-name"].strip()
        task_customer_id = request.POST["select-task-customer"].strip()
        task_date = request.POST["task-date"].strip()
        task_price = float(request.POST["task-price"].strip())

        # Check task name
        if len(task_name) < 2:
            return render(request, "crm_system/tasks.html", {
                "message": "Task name is to short."
            })
        elif len(task_name) > 50:
            return render(request, "crm_system/tasks.html", {
                "message": "Task name must be only 50 characters long."
            })

        # Check the task date
        if datetime.datetime.strptime(task_date, "%Y-%m-%d") < datetime.datetime.today():

            return render(request, "crm_system/tasks.html", {
                "message": "Task finish date is wrong."
            })

        # Check task price
        if task_price < 0:

            return render(request, "crm_system/tasks.html", {
                "message": "Task price is negative."
            })

        # Two decimal places and convert to string
        task_price = str(format(float(task_price), '.2f'))

        # Calculate the id for the new task of the authenticated user
        task_count = Task.objects.all().filter(task_to_user=request.user)
        task_counter = 1
        try:
            for _ in task_count:
                task_counter += 1
        except:
            task_counter = 1

        # Save new task if all intern restrictions was passed
        new_task = Task(task_id=task_counter, task_customer_id=Customer.objects.all().filter(to_user=request.user).get(customer_id=task_customer_id), task_name=task_name, task_date=task_date, task_price=task_price, task_to_user=request.user)
        new_task.save()

        # Render taks page
        return HttpResponseRedirect(reverse("tasks_view"))

    else:
        # Get all customers for authenticated user
        customer_list = Customer.objects.all().filter(to_user=request.user).order_by("last_name")

        # Get all taks for authenticated user and not done
        data = Task.objects.all().filter(task_to_user=request.user, task_done=False)

        # Pagination
        # Choose how much posts per page
        p = Paginator(data, 5)
        # Get the posts
        task_list = p.get_page(request.GET.get('page'))

        return render(request, "crm_system/tasks.html", {
            "customer_list": customer_list,
            "page_obj": task_list
        })


# Customer info page
@login_required(login_url='/crm_system/login.html')
def customers_info(request, customer_info_id):

    # Get current customer object
    current_customer = Customer.objects.get(pk=customer_info_id)

    # Check permission
    if current_customer not in Customer.objects.all().filter(to_user=request.user):
        return render(request, "crm_system/customer.html", {
            "message": "This is not your customer!"
        })

    return render(request, "crm_system/customer_info.html", {
        "current_customer": current_customer
    })


# Edited customer info box content
@login_required(login_url='/crm_system/login.html')
def edit_customer_info_box(request):

    # Get customer info box edited content from page by fetch
    edited_info_box_content = json.loads(request.body)

    # Get the customer info box to edit from the database
    old_info_box_content = Customer.objects.get(pk=edited_info_box_content["customer_id"])

    # Save the edited entry in database
    old_info_box_content.info_box = edited_info_box_content["edited_content"]
    old_info_box_content.save()

    # Get current customer object
    current_customer = Customer.objects.get(pk=edited_info_box_content["customer_id"])

    # Return successfully if all was done
    return JsonResponse({"message": "Info box edited successfully."}, status=201)


# Task info page
@login_required(login_url='/crm_system/login.html')
def task_info(request, task_info_id):

    # Get current customer object
    task = Task.objects.get(pk=task_info_id)
    current_customer = Customer.objects.all().filter(to_user=request.user).get(customer_id=task.task_customer_id.customer_id)

    # Get current task object
    current_task = Task.objects.get(pk=task_info_id)

    # Check permission
    if current_task not in Task.objects.all().filter(task_to_user=request.user):
        return render(request, "crm_system/tasks.html", {
            "message": "This is not your customer!"
        })

    # Render task info page
    return render(request, "crm_system/task_info.html", {
        "current_task": current_task,
        "current_customer": current_customer
    })

# Task done process
@login_required(login_url='/crm_system/login.html')
def task_done(request):

    if request.method == "POST":

        # Get data from page task id whch is done
        task_done_id = request.POST["task_done_id"]

        # Get the current task object
        current_task = Task.objects.get(pk=task_done_id)

        # Set task done to True, task date to now and save
        current_task.task_done = True
        current_task.task_done_date = datetime.date.today()
        current_task.save()

        # Get customer for the task bill
        current_customer = Customer.objects.all().filter(to_user=request.user).get(customer_id=current_task.task_customer_id.customer_id)

        # Generate a PDF bill
        buf = io.BytesIO()
        pdf = canvas.Canvas(buf, "Bill.pdf")
        pdf.setTitle("Bill")

        # Title
        pdf.setFillColorRGB(0.8, 0.8, 0.8)
        pdf.setFont("Helvetica-Bold", 36)
        pdf.drawCentredString(300, 760, "Bill")

        # Draw line beneath title
        pdf.setStrokeColor(colors.grey)
        pdf.line(255, 750, 350, 750)

        # Second header
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 28)
        pdf.drawCentredString(300, 650, "Bill for Task " + current_task.task_name)
        pdf.drawCentredString(300, 610, "for " + current_customer.first_name + " " + current_customer.last_name)

        # Task done date
        pdf.setFillColorRGB(0, 1, 0)
        pdf.drawCentredString(300, 500, "Task done on: " + str(current_task.task_done_date))

        # Task price
        pdf.setFillColorRGB(0.8, 0.2, 0.3)
        pdf.drawCentredString(300, 400, "Price: " + str(current_task.task_price) + " €")

        # Last sentence of the bill
        pdf.setFillColorRGB(0, 0, 1)
        pdf.drawCentredString(300, 200, "Thanks for your trust in our corporation.")

        # Save and offer to download the pdf file
        pdf.showPage()
        pdf.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename="Bill.pdf")

    else:
        return HttpResponseRedirect(reverse("tasks_view"))


# Archive of all tasks which are done
@login_required(login_url='/crm_system/login.html')
def tasks_archive(request):

    # Get all taks for authenticated user and done
    data = Task.objects.all().filter(task_to_user=request.user, task_done=True).order_by("-task_id")

    # Pagination
    # Choose how much posts per page
    p = Paginator(data, 5)
    # Get the posts
    task_list = p.get_page(request.GET.get('page'))

    return render(request, "crm_system/tasks_archive.html", {
        "page_obj": task_list
    })


