from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.db.models import Min, Max
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Category, Brand, Product, Order, OrderDetail, Promotion

# Create your views here.

def index(request):
    # Category parent, không lấy category con.
    categories = Category.objects.filter(category_parent__isnull=True)
    brands = Brand.objects.all()
    products = Product.objects.all()
    minimum_price = products.aggregate(Min('price'))
    maximum_price = products.aggregate(Max('price'))
    #print(maximum_price['price__max'], minimum_price['price__min'])
    category_search = request.GET.get('category')
    category_display = ''
    brand_display = ''
    if category_search:
        category_display = Category.objects.get(name=category_search)
        products = Product.objects.filter(category=category_display)
    brand_search = request.GET.get('brand')
    if brand_search:
        brand_display = Brand.objects.get(name=brand_search)
        products = Product.objects.filter(brand=brand_display)
    product_promtions = Promotion.objects.filter(
        start_date__lte=now(), # Ngày bắt đầu kmai < Ngày hiện tại (trước ngày hiện tại)
        end_date__gt=now()
    )
    return render(
        request=request,
        template_name='index.html',
        context={
            'categories': categories,
            'brands': brands,
            'category_display': category_display,
            'brand_display': brand_display,
            'products': products,
            'maximum_price': maximum_price['price__max'], 
            'minimum_price': minimum_price['price__min'],
            'product_promtions': product_promtions
        }
    )

@login_required(login_url='/user/login')   
def view_product(request, product_id):
    try:
        product_data = Product.objects.get(id=product_id)
        return render(
            request=request, 
            template_name='product/product-details.html',
            context={
                'product_data': product_data
            }
        )
    except Product.DoesNotExist:
        return render(request=request, template_name='404.html')

@login_required(login_url='/user/login')    
def add_product_to_cart(request, product_id):
    try:
        # Xác định về người đăng nhập
        logged_user = request.user
        product_data = Product.objects.get(id=product_id)
        # Kiễm tra xem người dùng có giỏ hàng nào chưa thành công (status = 0)
        user_has_ordered = Order.objects.get(user=logged_user, status=0) # status=0 là chưa thành công
        
        # Người dùng có 1 order chưa thành công.
        # Chia 2 trường hợp
        # Người dùng thêm 1 sản phẩm không trùng với các có trong giỏ hàng. Thêm mới 1 dòng OrderDetail với sản phẩm mới 
        
        # Người dùng thêm sản phầm trùng với sản phẩm đã có trong giỏ hàng. Cập nhập dòng OrderDetail với sản phẩm đó và tăng quantity lên 1order = user_has_ordered # ĐỔi tên lại cho dể xử lý
        order = user_has_ordered
        orderdetail = OrderDetail.objects.get(order=order, product=product_data)
        #orderdetail = order.orderdetail_set.get(product=product_data)
        # Qua dòng này thì đồng nghĩa là sản phẩm thêm mới trùng với 1 trong các sản phẩm trong giỏ hàng.
        # Tăng quantity += 1
        orderdetail.quantity += 1
        orderdetail.amount = orderdetail.quantity * product_data.price
        orderdetail.save()
    except Product.DoesNotExist:
        pass
    except Order.DoesNotExist:
        # Rớt vào except thì người dùng không đơn hàng chưa thành công. (Không có gì luôn hoặc có đơn hàng mà kiểu như thanh toán rồi status=1)
        
        # Tạo mới 1 Order với logged_user
        new_order = Order.objects.create(
            user=logged_user,
            status=0,
            create_date=now(),
            total_amount=0,
            phone="",
            address=""
        )
        # Order không có thông tin về sản phẩm, nên tạo tiếp 1 OrderDetail
        OrderDetail.objects.create(
            product=product_data,
            order=new_order,
            quantity=1,
            amount=product_data.price
        )
    except OrderDetail.DoesNotExist:
        # Người dùng thêm 1 sản phẩm không trùng với các có trong giỏ hàng. Thêm mới 1 dòng OrderDetail với sản phẩm mới
        OrderDetail.objects.create(
            product=product_data,
            order=order,
            quantity=1,
            amount=product_data.price
        )
    user_ordered = Order.objects.get(user=logged_user, status=0) # Đếm sản phẩm của đơn hàng chưa thành công
    quantity = sum([item.quantity for item in user_ordered.orderdetail_set.all()])
    return JsonResponse(data={'quantity': quantity})

# 2 hàm views để tăng hoặc giảm
# def increase_quantity
# def decrease_quantity

# Viết 1 hàm nhưng hổ trợ cả tăng/giảm sản phẩm, 1 hàm sẽ có tới 2 tham số
@login_required(login_url='/user/login')    
def change_product_quantity(request, action, product_id):
    # action: increase/decrease
    # Xác định về người đăng nhập
    logged_user = request.user
    product_data = Product.objects.get(id=product_id)
    order = Order.objects.get(user=logged_user, status=0)
    orderdetail = OrderDetail.objects.get(order=order, product=product_data)
    if action == 'increase':
        orderdetail.quantity += 1
        orderdetail.amount = orderdetail.quantity * product_data.price
        orderdetail.save()
    else:
        # decrease
        if orderdetail.quantity == 1:
            orderdetail.delete()
            # print("Xóa: ", product_data.name)
        # Giảm tới quantity == 1, bấm thêm 1 lần nữa thì đống nghĩa xóa sản phẩm ra khỏi giỏ hàng
        else:
            orderdetail.quantity -= 1
            orderdetail.amount = orderdetail.quantity * product_data.price
            orderdetail.save()
    return redirect('show_cart')

@login_required(login_url='/user/login')
def delete_product_in_cart(request, product_id):
    logged_user = request.user
    product_data = Product.objects.get(id=product_id)
    order = Order.objects.get(user=logged_user, status=0)
    orderdetail = OrderDetail.objects.get(order=order, product=product_data)
    orderdetail.delete()
    return redirect('show_cart')
        
@login_required(login_url='/user/login')
def show_cart(request):
    orderdetail = []
    message = ""
    total_amount = 0
    try:
        logged_user = request.user
        order = Order.objects.get(user=logged_user, status=0)
        orderdetail = order.orderdetail_set.all()
        if len(orderdetail) == 0:
            message = "Chưa có sản phẩm trong giỏ hàng"
        else:
            total_amount = sum([item.amount for item in orderdetail])
    except:
        message = "Chưa có sản phẩm trong giỏ hàng"
    return render(
            request=request, 
            template_name='cart/cart.html',
            context={
                'data_orderdetail': orderdetail,
                'message': message,
                'total_amount': total_amount
            }
        )

@login_required(login_url='/user/login')    
def checkout(request):
    orderdetail = []
    total_amount = 0
    logged_user = request.user
    order = Order.objects.get(user=logged_user, status=0)
    orderdetail = order.orderdetail_set.all()
    if request.method == "POST":
        phone = request.POST['phone']
        address = request.POST['address']
        order.phone = phone
        order.address = address
        order.total_amount = sum([item.amount for item in orderdetail])
        order.status = 1 # Đơn hành thành công
        order.save()
        for od_detail in orderdetail:
            od_detail.product.stock_quantity -= od_detail.quantity
            od_detail.product.save()
            
        from_email = settings.EMAIL_HOST_USER
#         subject = "Thanks for your checkout at shop django"
#         message = f''' Hi  {logged_user.username}
#     Thanks for your check out.
#     Total amount: {intcomma(order.total_amount)} đ
    
#     Thanks
#     shop django
# '''     
        text_content = 'This is an important message.'
        html_content = f'''
        <p> Hi  {logged_user.username}
    Thanks for your check out.</p

        <p>Here is detail your order:</p>
                <table class="table table-condensed">
				<thead>
					<tr class="cart_menu">
						<td class="description">Name</td>
						<td class="price">Price</td>
						<td class="quantity">Quantity</td>
						<td class="total">Total</td>
					</tr>
				</thead>
				<tbody>
''' 
        for od_detail in orderdetail:
            html_content += f'''
            <tr>
                <td class="cart_description">
                    <h4>{ od_detail.product.name }</h4>
                </td>
                <td class="cart_price">
                    <p>{ intcomma(od_detail.product.price) }đ</p>
                </td>
                <td class="cart_quantity">
                    <div class="cart_quantity_button">
                        {od_detail.quantity}
                    </div>
                </td>
                <td class="cart_total">
                    <p class="cart_total_price">{ intcomma(od_detail.amount)}đ</p>
                </td>
            </tr>
'''
        html_content += f'''
				</tbody>
			</table>
   
        <p>Total amount: <b>{intcomma(order.total_amount)} đ</b></p>
    
        <p>Thanks,</p>
        <p>shop django</p>
        '''
        recipient_list = [logged_user.email]
        # send_mail(subject, message, from_email, recipient_list)
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('index')
    return render(
        request=request, 
        template_name='cart/checkout.html',
        context={
            'data_orderdetail': orderdetail,
            'total_amount': total_amount
        }
    )