from django.shortcuts import render

def product_page(request):
    return render(request, "products.html")