from django.db import models

# Create your models here.


class register(models.Model):
    uname = models.CharField(max_length=20)
    email = models.EmailField()
    uphno = models.IntegerField()
    img = models.FileField()
    usname = models.CharField(max_length=10,unique=True)
    pwd = models.CharField(max_length=10)
    addrs = models.CharField(max_length=100)
    dist = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pncd = models.IntegerField()

class add_product(models.Model):
    pro_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    quantity = models.IntegerField()
    price = models.IntegerField()
    pro_img = models.FileField()


class Cart(models.Model):
    product_details = models.ForeignKey(add_product,on_delete=models.CASCADE)
    user_details = models.ForeignKey(register,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()

class Wishlist(models.Model):
    user_details = models.ForeignKey(register,on_delete=models.CASCADE)
    item_details = models.ForeignKey(add_product,on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    status = models.IntegerField(default=0)
class d_register(models.Model):
    df_name = models.CharField(max_length=10)
    dl_name = models.CharField(max_length=15)
    d_email = models.EmailField()
    d_adrs = models.CharField(max_length=50)
    d_phno = models.IntegerField()
    d_img = models.FileField()
    d_lcnc = models.FileField()
    d_bio = models.FileField()
    d_username = models.CharField(max_length=10, unique=True)
    d_password = models.CharField(max_length=10)
class Order(models.Model):
        customer = models.ForeignKey(register, on_delete=models.CASCADE)
        cart_details = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True,
                                         blank=True)  # Adjust according to your requirements
        product = models.ForeignKey(add_product, on_delete=models.CASCADE)
        so_fname = models.CharField(max_length=20, null=False)
        so_lname = models.CharField(max_length=20)
        so_email = models.EmailField(null=False)
        so_phone = models.IntegerField(null=False)
        so_address = models.TextField(null=False)
        so_district = models.CharField(max_length=20, null=False)
        so_city = models.CharField(max_length=20, null=False)
        so_pincode = models.IntegerField(null=False)
        add_message = models.CharField(max_length=250)
        order_status = (
            ('Pending', 'Pending'),
            ('Out For Shipping', 'Out For Shipping'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        )
        status = models.CharField(max_length=150, choices=order_status, default='Pending')
        quantity = models.IntegerField(null=False)
        total_price = models.FloatField(null=False)
        payment_mode = models.CharField(max_length=150, null=False)
        payment_id = models.CharField(max_length=150, null=True)
        order_id = models.CharField(max_length=150, null=False)
        tracking_no = models.CharField(max_length=150, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        delivery_boy = models.ForeignKey(d_register, on_delete=models.CASCADE, null=True, )


class PasswordReset(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE, null=True, blank=True)
    emp = models.ForeignKey(d_register, on_delete=models.CASCADE, null=True, blank=True)
    # security
    token = models.CharField(max_length=4)
