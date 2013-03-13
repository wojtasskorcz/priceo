from django import forms
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from priceo.models import Category, Product

CATEGORY_CHOICES = [("all", "All categories")]
CATEGORY_CHOICES.extend([(category.id, category.name) for category in Category.objects.all()])

class SearchForm(forms.Form):
    query = forms.CharField(initial=settings.SEARCH_DEFAULT_TEXT)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    
def results(request, order_by):
    # there have to be the GET parameters passed in the url every time this view is called
    # use ?{{ request.GET.urlencode }} in template to pass the previous GET to the view
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            category_id = form.cleaned_data['category']
            if category_id == "all":
                results = [product for product in Product.objects.all() 
                        if query.lower() in product.name.lower()]
            else:
                category = Category.objects.get(pk=category_id)
                results = [product for product in Product.objects.filter(category=category) 
                        if query.lower() in product.name.lower()]
    if order_by == "price" or order_by == "-price":
        results = sorted(results, key = lambda product : product.lowest_possible_price())
        if order_by == "-price":
            results.reverse()
    elif order_by == "rating" or order_by == "-rating":
        results = sorted(results, key = lambda product : product.get_thumbs_up() - product.get_thumbs_down())
        if order_by == "-rating":
            results.reverse()
    elif order_by == "name" or order_by == "-name":
        results = sorted(results, key = lambda product : product.name)
        if order_by == "-name":
            results.reverse()
    elif order_by == "pub_date" or order_by == "-pub_date":
        results = sorted(results, key = lambda product : product.pub_date)
        if order_by == "-pub_date":
            results.reverse()
    paginator = Paginator(results, settings.RESULTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request, 'search/results.html',
                  {'results': results,
                   'order_by': order_by})