from priceo.models import Category, Product
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

def category_details(request, category_id, order_by):
    category = get_object_or_404(Category, pk=category_id)
    products = category.products.all()
    if order_by == "price" or order_by == "-price":
        products = sorted(products, key = lambda product : product.lowest_possible_price())
        if order_by == "-price":
            products.reverse()
    elif order_by == "rating" or order_by == "-rating":
        products = sorted(products, key = lambda product : product.get_thumbs_up() - product.get_thumbs_down())
        if order_by == "-rating":
            products.reverse()
    else:
        products = products.order_by(order_by)
    paginator = Paginator(products, settings.RESULTS_PER_PAGE) # Show 5 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    return render(request, 'categories/category_details.html', {"products": products,
                                                       "category": category,
                                                       "order_by": order_by})
    