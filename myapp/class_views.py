from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Pet
from .forms import PetForm

# R: READ all
class PetListView(ListView):
    # `model` attrivute định nghĩa tạo list view cho model nào ?
    # queryset = Pet.objects.all()
    # NOTE: 
    # 1. Dùng ListView thì phải tạo ra thuộc tính `model` hoặc `query` 
    # hoặc ghi đè phương thức `get_queryset()`
    # 2. Template mặc định mà render `tên app\tên class_list.html`
    #    Thay thế template mặc định, thêm biến `template_name= template.html`
    # 3. Tên context mặc định bên template có là `object_list`
    #    Thay thế bằng 1 tên  gợi nhớ khác, thêm biến `context_object_name`
    model = Pet
    template_name = 'class/index.html'
    context_object_name = 'pets'
    # PHÂN TRANG: số lượng item hiển thi. Còn những thông ẩn đi thì chuyển qua trang tiếp theo
    paginate_by = 5 # số item trên 1 trang
    def get_queryset(self):
        pets = Pet.objects.all()
        search = self.request.GET.get('search')
        if search:
            pets = Pet.objects.filter(name__icontains=search)
        return pets

@method_decorator(login_required(login_url='/user/login'), name="dispatch")
class PetDetailView(DetailView):
    # Template mặc định mà render `tên app\tên class_detail.html`
    #    Thay thế template mặc định, thêm biến `template_name= template.html`
    # Tên context mặc định bên template có là `object`
    #    Thay thế bằng 1 tên  gợi nhớ khác, thêm biến `context_object_name`
    model = Pet
    template_name = 'class/detail.html'
    context_object_name = 'pet'

@method_decorator(login_required(login_url='/user/login'), name="dispatch")
class PetCreateView(CreateView):
    # Template mặc định mà render `tên app\tên class_form.html`
    #    Thay thế template mặc định, thêm biến `template_name= template.html`
    # Tên context mặc định bên template có là `form` nếu xài form
    #    Thay thế bằng 1 tên  gợi nhớ khác, thêm biến `context_object_name`
    model = Pet
    # CreateView cần có fields: (tương tự như forms)
    # fields = '__all__'
    # Không có fields thì xài `form_class = Tên Form`
    form_class = PetForm
    template_name = 'class/add.html'
    success_url = reverse_lazy('class_index')

@method_decorator(login_required(login_url='/user/login'), name="dispatch")
class PetUpdateView(UpdateView):
    model = Pet
    # UpdateView cần có fields: (tương tự như forms)
    # fields = '__all__'
    # Không có fields thì xài `form_class = Tên Form`
    form_class = PetForm
    # Template mặc định mà render `tên app\tên class_form.html`
    #    Thay thế template mặc định, thêm biến `template_name= template.html`
    # Tên context mặc định bên template có là `form` nếu xài form
    template_name = 'class/update.html'
    success_url = reverse_lazy('class_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet_id'] = self.object.id
        return context

@method_decorator(login_required(login_url='/user/login'), name="dispatch")
class PetDeleteView(DeleteView):
    model = Pet
    # Template mặc định mà render `tên app\tên class_confirm_delete.html`
    template_name = 'class/confirm_delete.html'
    success_url = reverse_lazy('class_index')