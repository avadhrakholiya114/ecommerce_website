import razorpay
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .models import product, Customer, cart, payment, orderplaced
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import customerform
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import random
from django.template import loader
import pdfkit


# Create your views here.
# avadh8


def home(request):
    # get all product
    pro = product.objects.all()
    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()


    if request.GET.get('search'):
        search = request.GET.get('search')

        pro = product.objects.filter(
            Q(title__icontains=search) |
            Q(selling_price__icontains=search) |
            Q(discounted_price__icontains=search) |
            Q(catagory__icontains=search) |
            Q(color=search)

        )

        return render(request, 'search.html', locals())

    # context = {'pro': pro,
    #
    #            }
    return render(request, 'home.html', locals())


def detail(request, id):

    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()
    pro_detail = product.objects.get(id=id)
    # return render(request, 'detail.html', {'pro_detail': pro_detail, 'ca': ca})
    return render(request, 'detail.html', locals())


def register(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')

        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        Conform_Password = request.POST.get('Conform_Password')

        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
            messages.warning(request, "email Already Exists.")
            return HttpResponseRedirect(request.path_info)
        if password != Conform_Password:
            messages.warning(request, "Password Must Be Match.")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name=first_name, last_name=last_name, username=email, email=email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Your Account Has Been Created plz Login Here.")
        return HttpResponseRedirect('/login_user/')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, "Invalid Credntials.")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/profile/')

        messages.warning(request, "password not match.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'login.html')


def Logout_user(request):
    logout(request)
    return redirect('/login_user/')


@login_required(login_url="/login_user/")
def profile(request):
    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = customerform(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, zipcode=zipcode,
                           state=state)
            reg.save()
            return redirect('/address/')
    form = customerform()
    return render(request, 'profile.html', {'form': form, 'ca': ca})


@login_required(login_url="/login_user/")
def address(request):
    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add': add, 'ca': ca})


@login_required(login_url="/login_user/")
def update(request, id):
    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()
    if request.method == 'POST':
        form = customerform(request.POST)
        if form.is_valid():
            data = Customer.objects.get(id=id)
            data.name = form.cleaned_data['name']
            data.locality = form.cleaned_data['locality']
            data.city = form.cleaned_data['city']
            data.mobile = form.cleaned_data['mobile']
            data.zipcode = form.cleaned_data['zipcode']
            data.state = form.cleaned_data['state']
            data.save()
            return redirect('/address/')
    data = Customer.objects.get(id=id)
    form = customerform(instance=data)
    return render(request, 'update.html', {'form': form, 'ca': ca})


@login_required(login_url="/login_user/")
def addtocart(request, id):
    user = request.user
    pro = product.objects.get(id=id)
    che = cart.objects.filter(product__id=id)
    if che:
        messages.warning(request, "Cart Already Exists")
        return redirect('/show_cart/')
    else:
        cart(user=user, product=pro).save()
        messages.success(request, "Cart Item Added Successfully")
        return redirect('/show_cart/')


@login_required(login_url="/login_user/")
def show_cart(request):
    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()
    user = request.user
    data = cart.objects.filter(user=user)
    # total amount count
    total = 0
    for p in data:
        value = p.quantity * p.product.discounted_price
        total = total + value
    totalamount = total + 40
    context = {
        'total': total,
        'data': data,
        'totalamount': totalamount,
        'ca': ca
    }
    return render(request, 'cart.html', context)


def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        # data={
        # }
        # return JsonResponse(data)
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        # fari var total karvu pade ne so
        user = request.user
        data = cart.objects.filter(user=user)
        # total amount count
        total = 0
        for p in data:
            value = p.quantity * p.product.discounted_price
            total = total + value
        totalamount = total + 40
        data = {
            'quantity': c.quantity,
            'total': total,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity < 1:
            c.delete()

        else:
            c.quantity -= 1
            c.save()
            user = request.user
            data = cart.objects.filter(user=user)
            # total amount count
            total = 0
            for p in data:
                value = p.quantity * p.product.discounted_price
                total = total + value
            totalamount = total + 40
            data = {
                'quantity': c.quantity,
                'total': total,
                'totalamount': totalamount
            }
            return JsonResponse(data)


def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']

        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        c.delete()

        user = request.user
        data = cart.objects.filter(user=user)
        # total amount count
        total = 0
        for p in data:
            value = p.quantity * p.product.discounted_price
            total = total + value
        totalamount = total + 40
        data = {

            'total': total,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required(login_url="/login_user/")
def checkout(request):
    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()
    data = cart.objects.filter(user=request.user)
    total = 0
    for p in data:
        value = p.quantity * p.product.discounted_price
        total = total + value
    totalamount = total + 40

    # for razorpay
    razoramount = int(totalamount * 100)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    k = {'amount': razoramount, "currency": 'INR', "receipt": "order_rcptid_12"}
    paymant_response = client.order.create(data=k)
    # print(paymant_response)

    order_id = paymant_response['id']
    order_status = paymant_response['status']
    if order_status == 'created':
        pay = payment(
            user=request.user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status,

        )
        pay.save()

    # ------------------------
    add = Customer.objects.filter(user=request.user)
    context = {
        'data': data,
        'total': total,
        'totalamount': totalamount,
        'add': add,
        'razoramount': razoramount,
        'order_id': order_id,
        'ca': ca
    }
    return render(request, 'checkout.html', context)


@login_required(login_url="/login_user/")
def paymentdone(request):
    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")
    cust_id = request.GET.get("cust_id")

    user = request.user
    cus = Customer.objects.get(id=cust_id)

    pay = payment.objects.get(razorpay_order_id=order_id)
    pay.paid = True
    pay.razorpay_payment_id = payment_id
    pay.save()
    data = cart.objects.filter(user=request.user)
    for c in data:
        orderplaced(user=user, Customer=cus, product=c.product, quantity=c.quantity, payment=pay).save()
        c.delete()
    return redirect('/invoice/')


@login_required(login_url="/login_user/")
def order(request):
    if request.user.is_authenticated:
        ca = cart.objects.filter(user=request.user).count()
    order = orderplaced.objects.all()

    return render(request, 'order.html', {'order': order, 'ca': ca})

import io
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from xhtml2pdf import pisa
from io import BytesIO

@login_required(login_url="/login_user/")
def invoice(request):
    data = orderplaced.objects.filter(user=request.user)
    # print(data)

    total = 0
    for p in data:
        value = p.quantity * p.product.discounted_price
        total = total + value
    totalamount = total + 40

    cus = orderplaced.objects.filter(user=request.user).first()

    rand_num = random.randrange(1000, 100000)
    template = get_template('invoice.html')

    context = {'data': data, 'totalamount': totalamount, 'cus': cus, 'rand_num': rand_num }

    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)  # , link_callback=fetch_resources)
    pdf = result.getvalue()

    filename = 'Invoice.pdf'
    to_emails = [request.user,]
    subject = "Invoice of your purchase"
    email = EmailMessage(subject, "this is the invoice of your purchase which you u buy from our website thank u..", from_email=settings.EMAIL_HOST_USER, to=to_emails)
    email.attach(filename, pdf, "application/pdf")
    email.send(fail_silently=False)


    return HttpResponse(result.getvalue(), content_type='application/pdf')

