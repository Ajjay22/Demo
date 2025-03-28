"""
URL configuration for accessories project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',views.index),
    path('about',views.about),
    path('computer',views.computer),
    path('laptop',views.laptop),
    path('product',views.product),
    path('contact',views.contact),
    path('login',views.login),
    path('logout',views.logout),
    path('register',views.register_view),
    path('adminhome',views.adminhome),
    path('userhome',views.userhome),
    path('add_product',views.add_prod),
    path('update/<int:id>',views.update),
    path('delete/<int:id>', views.delete),
    path('admin_productdisplay',views.admin_productdisplay),
    path('user_view',views.view_user),
    path('view_orders',views.admin_orderview),
    path('user_product_details',views.user_display_product),
    path('cart/', views.cart1),
    path('addcart/<int:id>', views.addcart),
    path('increment/<int:cart_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement/<int:cart_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('deletecart/<int:id>', views.remove_cart),
    path('wishlist/',views.display_wishlist),
    path('addwish/<int:id>',views.addwish),
    path('delete_wish/<int:id>',views.delete_wish),
    path('singles/<int:d>/', views.singles, name='single'),
    path('single_razor/<int:product_id>', views.single_razor, name='single_razor'),
    path('razor_pay/<int:price>', views.razorpaycheck),
    path('success', views.success, name='success'),
    path('checkout', views.checkout, name='checkout'),
    path('multiple_razor', views.multiple_razor, name='multiple_razor'),
    path('razor_pay2', views.razorpaycheck2),
    path('user_my_orders', views.my_ordrs),
    path("profile", views.view_profile),
    path("profileedit", views.edit_profile),
    path('edit', views.edit_view),
    path('cancel_order/<int:id>',views.cancel_order),
    path('delboy_reg', views.delboy_reg),
    path('delboy_home',views.delboy_home),
    path('delboy_view',views.delboy_view),
    path('assign_delivery_boy/<int:order_id>', views.assign_delivery_boy),
    path('del_order_view', views.del_view_orders),

    path('del_statusup/<sts>', views.del_statusup, name="del_statusup"),
    path('forgot_password', views.forgot_password, name="forgot"),
    path('reset/<token>', views.reset_password, name='reset_password'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
