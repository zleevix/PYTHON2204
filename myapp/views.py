from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from myapp.models import Student, Pet
from myapp.forms import PetForm
# Create your views here.
# View đầu tiên
# File views.py đóng vai trò là chữ C trong MVC.
# R: Read
def index(request):
    pets = Pet.objects.all()
    search = request.GET.get('search')
    if search:
        pets = Pet.objects.filter(name__icontains=search)
    paginator = Paginator(object_list=pets, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    message = "Không có Pet" if len(pets) == 0 else ""
    return render(
        request=request,
        template_name='pet/index.html',
        context={
            'pets': pets,
            'message': message,
            'page_obj': page_obj
        }
    )

# C: CREATE
# Người phải đăng nhập thì mới add đc pet
@login_required(login_url='/user/login')
def add_pet(request):
    logged_user = request.user
    print(logged_user.has_perm('myapp.add_pet'))
    form = PetForm()
    if request.method == "POST":
        # Validation form
        # Server validation
        # form.save() # Giống model save()
        form = PetForm(request.POST)
        # return redirect('index')
        if form.is_valid(): # server validate có sẳn
            # print("Validate OK")
            form.save() # Giống model save()
            return redirect('index')
        # else:
        #     print("Lỗi")
        #     print(form.errors)
     
    return render(
        request=request,
        template_name='pet/add.html',
        context={
            'form': form
        }
    )

# U: UPDATE
@login_required(login_url='/user/login')
def update_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    form = PetForm(instance=pet)
    if request.method == "POST":
        form = PetForm(request.POST, instance=pet)
        # print(request.POST)
        # form.save()
        # return redirect('index')
        if form.is_valid():
            form.save()
            return redirect('index')
        # else:
        #     print("Lỗi")
        #     print(form.errors)
    return render(
        request=request,
        template_name='pet/update.html',
        context={
            'form': form,
            'pet_id': pet_id
        }
    )

#V: Views
@login_required(login_url='/user/login')
def detail_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    form = PetForm(instance=pet)
    return render(
        request=request,
        template_name='pet/detail.html',
        context={
            'form': form
        }
    )

# D: DELETE
@login_required(login_url='/user/login')
def delete_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet.delete()
    return redirect('index')

# def students(request):
#     students = Student.objects.all()
#     # response = HttpResponse()
#     # response.write("<h1>Danh sách các Student trong database</h1>")
#     # response.write("<ol>")
#     # for student in students:
#     #     response.write(f"<li>Name: {student.name}, Age: {student.age} </li>")
#     # response.write("</ol>")
#     return render(
#         request=request,
#         template_name='students.html',
#         context={
#             'students': students # key <tên biến sẽ dùng bên HTML>: value <value là giá trị biến bên python truyền vào>
#         }#Biến được truyền từ views sang template HTML.
#     )

# def add_student(request):
#     if request.method == "POST":
#         Student.objects.create(
#             name=request.POST['name'],
#             age=int(request.POST['age']),
#             gender=request.POST['gender']=="True",
#             email=request.POST['email'],
#             phone=request.POST['phone']
#         )
#         return redirect('students')
#         # return HttpResponseRedirect('/myapp/students')
#     return render(
#         request=request, 
#         template_name='add_student.html'
#     )
# # 2 cách
# # Function base view - class base view
# def my_view(request): # Hàm trong views.py sẽ luôn có 1 tham số phải có
#     # request: HTTP Request
#     # respone = HttpResponse()
#     # respone.write("<h1>Hello các bạn lớp PYTHON2204</h1>")
#     # respone.write("<p style='color:blue'>Đây là nội dung của my view</p>")
#     # Phải trả về là HTTP Response
#     # 65535
#     # <1024 là hệ thống.
#     if request.method == "POST":
#         request.session['username'] = request.POST['name-username']
#     return render(request, 'myview.html')

# # Thứ tự các bạn dùng để tạo 1 view mới trong Django
# # Bước 1: Tạo hàm trong `view.py`
# def welcome(request):
#     response = HttpResponse()
#     response.write(f"Welcome {request.session['username']}")
#     return response
