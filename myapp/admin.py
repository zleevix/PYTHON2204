from django.contrib import admin
from myapp.models import Student, Place, Restaurant, Reporter, Article
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email') # Những cột mà sẽ hiển thị trên giao diện admin khi quản class đó

class ArticleInlne(admin.StackedInline):
    model = Article

class ReporterAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email')
    inlines =[ArticleInlne]

    @admin.display(description='Full name')
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('headline', 'pub_date', 'reporter_id')

admin.site.register(Student, StudentAdmin)
admin.site.register(Place)
admin.site.register(Restaurant)
admin.site.register(Reporter, ReporterAdmin)
admin.site.register(Article, ArticleAdmin)
# admin.site.register(Publication)
# admin.site.register(Article)
