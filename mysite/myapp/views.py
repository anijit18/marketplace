from django.shortcuts import render,redirect
from .models import Product,OrderDetail
from .forms import ProductForm,UserRegistrationForm
import json
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    products=Product.objects.all()
    return render(request, 'myapp/index.html', {'products':products})

def detail(request, id):
    product=Product.objects.get(id=id)
    return render(request, 'myapp/detail.html', {'product':product})

def create_product(request):

    if request.method=='POST':
        product_form=ProductForm(request.POST,request.FILES)
        if product_form.is_valid():
            new_product=product_form.save(commit=False)
            new_product.seller=request.user
            new_product.save()
            return redirect('index')

    # as ProductForm is a class, therefore we have to make an object or an instance of that class
    product_form=ProductForm()
    return render(request, 'myapp/create_product.html', {'product_form':product_form})

def product_edit(request,id):
    product=Product.objects.get(id=id)

    if product.seller != request.user:
        return redirect('invalid')
    
    product_form=ProductForm(request.POST or None, request.FILES or None, instance=product)
    
    if request.method == 'POST':
        if product_form.is_valid():
            product_form.save()
            return redirect('index')

    return render(request, 'myapp/product_edit.html', {'product_form': product_form, 'product': product})

def product_delete(request, id):
    product=Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
    if request.method == 'POST':
        product.delete()    
        return redirect('index')
    return render(request, 'myapp/delete.html', {'product':product})

def dashboard(request):
    products=Product.objects.filter(seller=request.user)
    return render(request,'myapp/dashboard.html',{'products':products})

def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)
        new_user=user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')
    user_form=UserRegistrationForm()
    return render(request, 'myapp/register.html', {'user_form':user_form})

def invalid(request):
    return render(request, 'myapp/invalid.html')

def create_checkout_session(request,id):

    orders = OrderDetail.objects.all()
    return render(request, 'myapp/order_detail.html', {'orders':orders})

    
    request_data=json.load(request.body)
    product=Product.objects.get(id=id)

    order=OrderDetail()
    order.customer_email=request_data['email']
    order.product=product
    order.amount=int(product.price)
    order.save()
    return 

def my_purchases(request):
    orders = OrderDetail.objects.all()
    return render(request, 'myapp/purchases.html', {'orders':orders})

def payment_success_view (request,id):
    order = get_object_or_404(OrderDetail, id=id)
    order.customer_email = request.user.email
    order.save()
    return render(request, 'myapp/payment_success.html', {'order':order})
