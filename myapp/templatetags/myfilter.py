from django import template
register = template.Library()

@register.filter
def make_capitalize(value):
    return value.upper()

# Hàm make_capitalize() có 1 tham số
# Khi gọi hàm ở tempalte thì tham số|make_capitalize

@register.filter
def is_empty_list(list_object):
    return len(list_object) == 0

@register.filter
def make_range(num):
    return range(1, num + 1)

@register.filter
def make_serial(current_page, index_loop):
    # số phần tử trên 1 trang 5 
    # current_page = 2
    # index_loop = 3
    # index trả về là 8 = index_loop + (số item trên 1 trang * (current_page - 1))
    return index_loop + ((current_page-1)*5)