from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
import random
from.models import *
import razorpay
# Create your views here.
def index(re):
    return render(re,'index.html')
def about(re):
    return render(re,'about.html')
def computer(re):
    return render(re,'computer.html')
def laptop(re):
    return render(re,'laptop.html')
def product(re):
    return  render(re,'product.html')
def contact(re):
    return render(re,'contact.html')

def login(re):
    if re.method=='POST':
        username=re.POST['username']
        password=re.POST['password']
        try:
            data=register.objects.get(usname=username)
            if username == data.usname and password == data.pwd:
                re.session['user'] = username
                return redirect(userhome)
            else:
                messages.error(re,'...Invalid Username or Password...')
        except Exception:
            try:
                data = d_register.objects.get(d_username=username)
                if username == data.d_username and password == data.d_password:
                    re.session['did'] = username
                    return redirect(delboy_home)
                else:
                    messages.error(re, '...Invalid Username or Password...')
            except:
                if username == 'admin' and password == 'admin123':
                    re.session['admin'] = username
                    return redirect(adminhome)
                else:
                    messages.error(re, '...Invalid Username or Password...')
    return render(re, 'login.html')
def logout(re):
    if 'user' in  re.session or 'admin' in re.session:
        re.session.flush()
        return redirect(login)
def register_view(request):
    if request.method== 'POST':
        uname = request.POST.get('name','')
        email = request.POST.get('email','')
        uphno = request.POST.get('nmbr','')
        img = request.FILES.get('user_img',None)
        addrs = request.POST.get('adrss','')
        dist = request.POST.get('udistrict','')
        city = request.POST.get('ucity','')
        pncd = request.POST.get('upincode',)
        usname = request.POST.get('usname','')
        pwd = request.POST.get('password','')
        try:
            u = register.objects.get(username=usname)
            if u is not None:
                messages.error(request,'...Username Already Exist....')
                return  redirect(request,register)
        except Exception:
            u = register.objects.create(uname=uname,email=email,uphno=uphno,img=img,addrs=addrs,dist=dist,city=city,pncd=pncd,usname=usname,pwd=pwd)
            u.save()
            messages.success(request,'...Register Details added Successfully...')
    return render(request,'register.html')
def adminhome(re):
    return render(re, 'adminhome.html')

def userhome(request):
    return render(request, 'userhome.html')
def add_prod(request):
    if 'admin' in request.session:
        if request.method=='POST':
            pname = request.POST['pname']
            description = request.POST['shrtdes']
            quantity = request.POST['quant']
            price = request.POST['price']
            pimg = request.FILES['pimg']
            product = add_product(pro_name=pname,description=description,quantity=quantity,price=price,pro_img=pimg)
            product.save()
            messages.success(request,'...product added successsfully...')
            return redirect(add_prod)
        return render(request,'add_product.html')
    return  redirect(adminhome)

def admin_productdisplay(re):
    if 'admin' in re.session:
        data=add_product.objects.all()
        return render(re,'admin_view.html',{'data':data})
    return redirect(login)

def admin_orderview(re):
    if 'admin' in re.session:
        data=Order.objects.all()
        de=d_register.objects.all()
        return render(re,'view_orders.html',{'order':data,'delivery':de})
    return redirect(login)


def user_display_product(request):
    if 'user' in request.session:
        data = add_product.objects.all()
        return render(request, 'user_product_details.html', {'data': data})
    return redirect(login)

def update(re, id):
    if 'admin' in re.session:
        data =add_product.objects.get(pk=id)
        print(data)
        if re.method == 'POST':
            a = re.POST['n1']
            b = re.POST['n2']
            c = re.POST['n3']
            add_product.objects.filter(pk=id).update(pro_name=a, price=b, quantity=c)
            return redirect(admin_productdisplay)
        return render(re, 'update.html', {'data': data})


def delete(request,id):
    if 'admin' in request.session:
        data=add_product.objects.get(pk=id)
        print(data)
        data.delete()
        return redirect(admin_productdisplay)
    return redirect(login)

def user_view(re):
    if 'user' in re.session:
        data=add_product.objects.all()
        return render(re,'user_view.html',{'data':data})
    return redirect(login)

def view_orders(re):
    if 'admin' in re.session:
        data = Order.objects.all()
        return render(re,'view_orders.html',{'order':data})
    return redirect(adminhome)

def view_profile(re):
    if 'user' in re.session:
        data = register.objects.get(usname=re.session['user'])
        return render(re, 'profile.html', {'user': data})
    return redirect(login)

def edit_profile(re):
    if 'user' in re.session:
        data = register.objects.get(usname=re.session['user'])
        return render(re, 'profileedit.html', {'user': data})
    return redirect(login)

def edit_view(re):
    if 'user' in re.session:
        if re.method=='POST':
            a = re.POST['name']
            b = re.POST['email']
            c = re.POST['username']
            register.objects.filter(usname=re.session['user']).update(name=a,email=b, usname=c)
            return redirect(view_profile)
            return render(re,'profileedit.html')
        return redirect(login)

def addcart(request, id):
        if 'user' in request.session:
            user = register.objects.get(usname=request.session['user'])
            data = add_product.objects.get(pk=id)
            if Cart.objects.filter(product_details=data, user_details=user).exists():
                d = Cart.objects.get(product_details=data, user_details=user)
                print("d=", d)
                d.quantity += 1
                print(d.quantity)
                d.save()
                return redirect(cart1)
            else:
                Cart.objects.create(product_details=data, user_details=user, total_price=data.price).save()
                print("hello")
                return redirect(user_display_product)
        return redirect(login)
def cart1(request):
    if 'user' in request.session:
        user = get_object_or_404(register,usname=request.session['user'])
        data=Cart.objects.filter(user_details=user)
        total_item=0
        amount=0
        for i in data:
            total_item+=1
            amount+=i.total_price
        return render(request,'cart.html',{'data':data,'amount':amount,'total_item':total_item})
    return redirect(login)
def decrement_quantity(request, cart_id):
    if 'user' in request.session:
        cart_item = get_object_or_404(Cart, id=cart_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.total_price = cart_item.quantity * cart_item.product_details.price
            cart_item.save()
        else:
            cart_item.delete()
    return redirect(cart1)

def increment_quantity(request, cart_id):
    if 'user' in request.session:
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.product_details.price
        cart_item.save()
    return redirect(cart1)

def remove_cart(request, id):
    if 'user' in request.session:
        cart_item = get_object_or_404(Cart, pk=id)
        cart_item.delete()
        messages.success(request, 'Item removed successfully')
    return redirect(cart1)
def wish(re):
    return render(re,'wishlist.html')

def addwish(re,id):
    if 'user' in re.session:
        u = register.objects.get(usname=re.session['user'])
        print(u)
        item = add_product.objects.get(pk=id)
        print(item)
        data = Wishlist.objects.create(item_details=item,user_details=u)
        data.save()
        messages.success(re,'...Product added to Wishlist...')
    return redirect(user_display_product)

def display_wishlist(re):
    if 'user' in re.session:
        details = register.objects.get(usname=re.session['user'])
        usr = register.objects.get(usname=details.usname)
        w = Wishlist.objects.all()
        l=[]
        for i in w:
            if i.user_details==usr:
                l.append(i)
        return render(re,'wishlist.html',{'l':l})
    return redirect(userhome)

def delete_wish(re,id):
    if 'user' in re.session:
        data = Wishlist.objects.get(pk=id)
        data.delete()
        messages.success(re,'...Item Removed....')
        return redirect(display_wishlist)

def singles(request, d):
    if 'user' in request.session:
        user = register.objects.get(usname=request.session['user'])
        product = add_product.objects.get(pk=d)
        return render(request, 'single_booking.html', {'udata': user, 'pdata': product})
    return redirect(userhome)



def single_razor(request, product_id):
    product = get_object_or_404(add_product, pk=product_id)
    user = get_object_or_404(register, usname=request.session['user'])
    crt = Cart.objects.filter(user_details=user).first()


    if request.method == "POST":
        print("hello")
        so_fname = request.POST.get('sofname', '')
        so_lname = request.POST.get('solname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        so_city = request.POST.get('scity', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('notes', '')
        quantity = int(request.POST.get('singleqty', 1))
        total_price_str = request.POST.get('total', '0')  # Get value, default to '0' if not found
        try:
            total_price = float(total_price_str)
        except ValueError:
            total_price = 0.0
        paymode = request.POST.get('payment_mode', '')
        print(paymode,total_price)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'meat' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'meat' + str(random.randint(1111111, 9999999))

        single_booking = Order.objects.create(
            customer=user,
            product=product,
            cart=crt,
            so_fname=so_fname,
            so_lname=so_lname,
            so_email=so_email,
            so_phone=so_phone,
            so_address=so_address,
            so_district=so_district,
            so_city=so_city,
            so_pincode=so_pincode,
            add_message=add_message,
            quantity=quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        single_booking.save()
        # if paymode == 'RazorPay':
        return redirect(razorpaycheck,product.price)
    #     return JsonResponse({'status': 'Your order has been placed successfully'})
    #
    # return redirect(usr_home)


# ---------------------------- RAZOR PAY ---------------------------

def razorpaycheck(request,price):
    if 'user' in request.session:
        u = register.objects.get(usname=request.session['user'])
        s = Order.objects.filter(customer=u)
        t = price*100
        return render(request, "payment.html", {'amount': t})

    return render(request, "payment.html")


def success(re):
    return redirect(my_ordrs)
# def my_ordrs(re):
#     pass
# ---------------------------- MULTIPLE BOOKING  ---------------------------

def checkout(request):
    # c = d
    mp = []
    t = 0
    if 'user' in request.session:
        user = register.objects.get(usname=request.session['user'])
        mp = Cart.objects.filter(user_details=user)
        c = mp
        t = 0
        print(mp)
        for i in c:
            t = t + (i.product_details.price * i.quantity)
        return render(request, 'multiple_booking.html', {'data': user, 'pdata':mp,'t':t})
    return redirect(userhome)




def multiple_razor(request):
    if 'user' not in request.session:
        return redirect(userhome)

    user = get_object_or_404(register, usname=request.session['user'])
    crt= Cart.objects.filter(user_details=user)
    t=0
    for i in crt:
        t = t + (i.product_details.price * i.quantity)
        total = t
        quty = i.quantity

    if crt.exists():
        crt_i = crt.first()
    else:
        messages.error(request, 'No cart found for the user')
        return redirect(userhome)


    if request.method == "POST":
        print("hello")
        m_fname = request.POST.get('sofname', '')
        m_lname = request.POST.get('solname', '')
        m_email = request.POST.get('semail', '')
        m_phone = int(request.POST.get('sphone', 10))
        m_address = request.POST.get('sadrs', '')
        m_district = request.POST.get('sdistrict', '')
        m_city = request.POST.get('scity', '')
        m_pincode = int(request.POST.get('spincode', 6))
        m_add_message = request.POST.get('notes', '')
        m_quantity = int(request.POST.get('singleqty', 1))
        m_quantity=quty
        # total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        # print(paymode,total_price)
        total_price =total
        product_id = crt_i.product_details.pk
        product = get_object_or_404(add_product, id=product_id)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'meat' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'meat' + str(random.randint(1111111, 9999999))
        for i in crt:
            multiple_booking = Order.objects.create(
                customer=user,
                product=i.product_details,
                cart_details=crt_i ,
                so_fname=m_fname,
                so_lname=m_lname,
                so_email=m_email,
                so_phone=m_phone,
                so_address=m_address,
                so_district=m_district,
                so_city=m_city,
                so_pincode=m_pincode,
                add_message=m_add_message,
                quantity=m_quantity,
                status='Pending',
                payment_mode=paymode,
                payment_id=None,
                order_id=order_id,
                tracking_no=tracking_no,
                total_price=total_price,
            )
        multiple_booking.save()
        # if paymode == 'RazorPay':
        messages.success(request, 'Your order has been placed successfully')

        return redirect(razorpaycheck2)
    return redirect(checkout)
 # In case the request method is not POST






def razorpaycheck2(request):
    if 'user' in request.session:
        u = register.objects.get(usname=request.session['user'])
        s = Order.objects.filter(customer=u)
        mp = Cart.objects.filter(user_details=u)
        c = mp
        t = 0
        print(mp)
        for i in c:
            t = t + (i.product_details.price * i.quantity)
            total = t * 100
        return render(request, "payment.html", {'amount': total})

    return render(request, "payment.html")

def my_ordrs(re):
    if 'user' in re.session:
        user = register.objects.get(usname=re.session['user'])
        order = Order.objects.filter(customer=user)
        return render(re, 'user_my_orders.html', {'pdata': order})
    return redirect(userhome)



# ---------------------------- CANSEL-BOOKING ---------------------------
def cancel_order(request,id):
    order = get_object_or_404(Order, id=id)
    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, 'Order has been successfully cancelled.')
    else:
        messages.info(request, 'Order is already cancelled.')
    return redirect(my_ordrs)

def delboy_reg(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        demail = request.POST['d_email']
        dadrs = request.POST['d_adrs']
        dphno = request.POST['d_nmbr']
        dimg = request.FILES['d_photo']
        dlcnc = request.FILES['d_licence']
        dbio = request.FILES['d_bio']
        dusname = request.POST['d_usname']
        dpwd = request.POST['d_password']
        try:
            d = d_register.objects.get(d_username=dusname)
            if d is not None:
                messages.error(request,'...Username Already Exist...')
        except Exception:
            d = d_register.objects.create(df_name=fname,dl_name=lname,d_email=demail,d_adrs=dadrs,d_phno=dphno,d_img=dimg,d_lcnc=dlcnc,d_bio=dbio,d_username=dusname,d_password=dpwd)
            d.save()
            messages.success(request,'...Profile Details added Successfully...')
    return render(request, 'delboy_reg.html')

def delboy_home(re):
    return render(re, 'delboy_home.html')




def logout(re):
    if 'user' in re.session and 'admin' in re.session and 'did' in re.session:
        re.session.flush()
        return redirect(login)
    return redirect(login)

def view_user(re):
    if 'admin' in re.session:
        data = register.objects.all()
        return render(re,'user_view.html',{'d':data})
    return redirect(adminhome)

def delboy_view(re):
    if 'admin' in re.session:
        data = d_register.objects.all()
        return render(re,'delboy_view.html',{'d':data})
    return redirect(adminhome)
def assign_delivery_boy(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        delivery_boy_id = request.POST.get('delivery_boy')
        if delivery_boy_id:
            try:
                delivery_boy = d_register.objects.get(id=delivery_boy_id)
                order.delivery_boy = delivery_boy
                order.status = 'Out For Shipping'
                order.save()
                messages.success(request, "Delivery boy assigned successfully.")
                return redirect(admin_orderview)  # Replace with the name of your URL pattern for admin orders
            except d_register.DoesNotExist:
                messages.error(request, "Delivery boy not found.")
                return redirect(admin_orderview)
        else:
            messages.error(request, "No delivery boy selected.")
            return redirect(admin_orderview)
    else:
        return HttpResponse("Invalid request method", status=405)


def del_view_orders(re):
    if 'did' in re.session:
        user = d_register.objects.get(d_username=re.session['did'])
        data = Order.objects.filter(delivery_boy=user)
        return render(re,'del_view_order.html',{'order' : data})
    return redirect(delboy_home)
def del_statusup(re,sts):
    if re.method == "POST":
        st = Order.objects.get(id=sts)
        st.status = re.POST.get('status')
        st.save()
    return redirect(del_view_orders)
# def delboy_view(re):
#     if 'admin' in re.session:
#         data = Order.objects.all()
#         return render(re,'del_view.html',{'order' : data})
#     return redirect(delboy_home)

from django.utils.crypto import get_random_string
from django.core.mail import send_mail

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        whois = request.POST.get('whois')
        try:
            user = register.objects.get(email=email)
        except register.DoesNotExist:
            user = None

        try:
            emp = d_register.objects.get(d_email=email)
        except d_register.DoesNotExist:
            emp = None

        if not user and not emp:
            return HttpResponse(
                 f"<script>alert('Email id not registered'); window.history.back();</script>",
                 content_type="text/html",
                 )


        if user:
            # Generate and save a unique token for the user
            token = get_random_string(length=4)
            PasswordReset.objects.create(user=user, token=token)
        else:
            # Generate and save a unique token for the employee
            token = get_random_string(length=4)
            PasswordReset.objects.create(emp=emp, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            return HttpResponse(
                f"<script>alert('We have sent you an email to change your current password'); window.history.back();</script>",
                content_type="text/html",
            )

        except:
            return HttpResponse(
                f"<script>alert('Network connection failed'); window.history.back();</script>",
                content_type="text/html",
            )

    return render(request, 'forget_password.html')


def reset_password(request, token):
        # Verify token and reset the password
        print(token)
        password_reset = PasswordReset.objects.get(token=token)
        # usr = User.objects.get(id=password_reset.user_id)
        if request.method == 'POST':
            new_password = request.POST.get('newpassword')
            repeat_password = request.POST.get('cpassword')

            if repeat_password == new_password:
                    try:
                        password_reset.user.pwd= new_password
                        password_reset.user.save()
                    except:
                        password_reset.emp.password = new_password
                        password_reset.emp.save()

                    # password_reset.delete()
                    return redirect(login)
            else:
                return HttpResponse(
                    f"<script>alert('Please recheck both your password'); window.history.back();</script>",
                    content_type="text/html",
                )

        return render(request, 'reset_password.html', {'token': token})






