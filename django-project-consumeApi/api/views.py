import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

FLASK_API_URL = "http://127.0.0.1:5000"

def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role", "user")

        payload = {"email": email, "password": password, "role": role}
        response = requests.post(f"{FLASK_API_URL}/register", json=payload)

        if response.status_code == 200:
            messages.success(request, "Registered successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, response.json().get("msg", "Registration failed"))

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        payload = {"email": email, "password": password}
        response = requests.post(f"{FLASK_API_URL}/login", json=payload)

        if response.status_code == 200:
            token = response.json().get("access_token")
            request.session['jwt_token'] = token
            messages.success(request, "Login successful!")
            return redirect('show_products')
        else:
            messages.error(request, response.json().get("msg", "Login failed"))

    return render(request, "login.html")

def show_products(request):
    token = request.session.get("jwt_token")
    if not token:
        return redirect('login')

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{FLASK_API_URL}/products", headers=headers)

    if response.status_code == 200:
        products = response.json()
    else:
        messages.error(request, "Failed to fetch products.")
        products = []

    return render(request, "products.html", {"products": products})

def add_product(request):
    token = request.session.get("jwt_token")
    if not token:
        return redirect('login')

    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        price = request.POST.get("price")

        headers = {"Authorization": f"Bearer {token}"}
        data = {"name": name, "category": category, "price": int(price)}
        response = requests.post(f"{FLASK_API_URL}/products", json=data, headers=headers)

        if response.status_code == 200:
            messages.success(request, "Product added successfully!")
            return redirect('show_products')
        else:
            messages.error(request, "Failed to add product.")

    return render(request, "add_product.html")
