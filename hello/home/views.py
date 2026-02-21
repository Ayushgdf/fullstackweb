from django.shortcuts import render, redirect
from home.models import about
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Get the user model (custom or default)
User = get_user_model()


# -------------------- PROTECTED VIEWS --------------------
@login_required(login_url='/?mode=login')
def about_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        feedback = request.POST.get('feedback')
        content = about(name=name, email=email, number=number, feedback=feedback)
        content.save()
    return render(request, "about.html")


@login_required(login_url='/?mode=login')
def services(request):
    return render(request, "services.html", {"user": request.user})


@login_required(login_url='/?mode=login')
def dash(request):
    return render(request, "dash.html", {"user": request.user})


@login_required(login_url='/?mode=login')
def model(request):
    return render(request, 'model.html')


# -------------------- LOGIN / SIGNUP --------------------
def index(request):
    mode = request.GET.get("mode", "login")
    next_url = request.GET.get("next")  # Remember which page user tried to access

    # If user already logged in, go to dashboard
    if request.user.is_authenticated:
        return redirect("dash")

    # Show info message if redirected due to login required
    if next_url:
        messages.info(request, "You must login or sign up to access the website 😊")

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # -------- LOGIN --------
        if form_type == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                # Redirect back to the page user wanted, or dashboard
                redirect_to = request.POST.get("next") or "dash"
                return redirect(redirect_to)
            else:
                messages.error(request, "Invalid credentials")
                return render(request, "sample.html", {"mode": "login"})

        # -------- SIGNUP --------
        elif form_type == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            phone = request.POST.get("phone", "")

            if not User.objects.filter(username=username).exists():
                if hasattr(User, 'phone') and phone:
                    User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        phone=phone
                    )
                else:
                    User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )

                messages.success(request, "Account created! Please login.")
                return redirect("/?mode=login")
            else:
                messages.error(request, "Username already exists")
                return render(request, "sample.html", {"mode": "signup"})

    # GET request → show login/signup page
    return render(request, "sample.html", {"mode": mode, "next": next_url})


# -------------------- LOGOUT --------------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("/")