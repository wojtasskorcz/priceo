from django import template
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db.models.loading import get_model
from priceo.models import Product, Category, ProductShop
from priceo.views.search import SearchForm
import random

def do_login_link(parser, token):    
    return LoginLinkNode()

class LoginLinkNode(template.Node):
    def render(self, context):
        user = context['user']
        if user.is_authenticated():
            return '<a href="%s">Log out, %s</a>' % (reverse('logout'), user.username)
        else:
            return '<a href="%s?next=%s">Log in</a> <a href="%s">Register</a>' % (reverse('login'), context['request'].get_full_path(), reverse('register'))
        
def do_latest_products(parser, token):
    bits = token.split_contents()
    if (len(bits) != 6 and len(bits) != 7) or bits[2] != 'from' or bits[len(bits)-2] != 'as':
        raise template.TemplateSyntaxError("'get_latest_products' tag takes exactly five or six arguments")
    number = bits[1]
    variable = bits[len(bits) -1]
    if len(bits) == 6:
        return AllLatestProductsNode(number, variable)
    elif len(bits) == 7: 
        model_args = bits[3].split('.')
        if len(model_args) != 2:
            raise template.TemplateSyntaxError("Third argument to 'get_latest_products' must be an 'application name'.'model name' string")
        model = get_model(*model_args)
        if model is None:
            raise template.TemplateSyntaxError("'get_latest_products' got an invalid model %s" % model_args)
        model_item_id = bits[4]
        return LatestProductsNode(number, model, model_item_id, variable)
    
class AllLatestProductsNode(template.Node):
    def __init__(self, number, variable):
        self.number = template.Variable(number)
        self.variable = variable
    def render(self, context):
        number = self.number.resolve(context)
        context[self.variable] = Product.objects.all().order_by('-pub_date')[:number]
        return ''

class LatestProductsNode(template.Node):
    def __init__(self, number, model, model_item_id, variable):
        self.number = template.Variable(number)
        self.model = model
        self.model_item_id = template.Variable(model_item_id)
        self.variable = variable
    def render(self, context):
        number = self.number.resolve(context)
        resolved_model_item_id = self.model_item_id.resolve(context)
        item = get_object_or_404(self.model, pk=resolved_model_item_id)
        context[self.variable] = item.products.all().order_by('-pub_date')[:number]
        return ''
    
def do_get_random_featured_products(parser, token):
    bits = token.split_contents()
    if (len(bits) != 6 and len(bits) != 7) or bits[2] != 'from' or bits[len(bits)-2] != 'as':
        raise template.TemplateSyntaxError("'get_random_featured_products' tag takes exactly five or six arguments")
    number = bits[1]
    variable = bits[len(bits) -1]
    if len(bits) == 6:
        return AllfeaturedProductsNode(number, variable)
    elif len(bits) == 7: 
        model_args = bits[3].split('.')
        if len(model_args) != 2:
            raise template.TemplateSyntaxError("Third argument to 'get_random_featured_products' must be an 'application name'.'model name' string")
        model = get_model(*model_args)
        if model is None:
            raise template.TemplateSyntaxError("'get_random_featured_products' got an invalid model %s" % model_args)
        model_item_id = bits[4]
        return FeaturedProductsNode(number, model, model_item_id, variable)
    
class AllfeaturedProductsNode(template.Node):
    def __init__(self, number, variable):
        self.number = template.Variable(number)
        self.variable = variable
    def render(self, context):
        number = self.number.resolve(context)
        products = Product.objects.filter(featured=True)
        random.shuffle(list(products))
        context[self.variable] = products[:number]
        return ''
    
class FeaturedProductsNode(template.Node):
    def __init__(self, number, model, model_item_id, variable):
        self.number = template.Variable(number)
        self.model = model
        self.model_item_id = template.Variable(model_item_id)
        self.variable = variable
    def render(self, context):
        number = self.number.resolve(context)
        resolved_model_item_id = self.model_item_id.resolve(context)
        item = get_object_or_404(self.model, pk=resolved_model_item_id)
        products = item.products.filter(featured=True)
        random.shuffle(list(products))
        context[self.variable] = products[:number]
        return ''
    
def do_show_categories(parser, token):
    return ShowCategoriesNode()

class ShowCategoriesNode(template.Node):
    def render(self, context):
        ret = '<ul>\n'
        for category in Category.objects.all():
            ret += '<li><a href="%s">%s</a></li>\n' % (reverse('category_details', args=(category.id,)), category.name)
        ret += '</ul>'
        return ret

def do_get_sorted_shops(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_sorted_shops' tag takes exactly three arguments")
    return SortedShopsNode(bits[1], bits[3])

class SortedShopsNode(template.Node):
    def __init__(self, product_id, variable):
        self.product_id = template.Variable(product_id)
        self.variable = variable
    def render(self, context):
        product_id = self.product_id.resolve(context)
        product = Product.objects.get(pk=product_id)
        shops = product.shops.all()
        context[self.variable] = sorted(shops, 
                key = lambda shop : ProductShop.objects.get(product__pk=product_id, shop__pk=shop.id).price)
        return ''

def do_get_url(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_url' tag take takes exactly two arguments")
    return UrlNode(bits[1], bits[2])

class UrlNode(template.Node):
    def __init__(self, product_id, shop_id):
        self.product_id = template.Variable(product_id)
        self.shop_id = template.Variable(shop_id)
    def render(self, context):
        product_id = self.product_id.resolve(context)
        shop_id = self.shop_id.resolve(context)
        return ProductShop.objects.get(product__pk=product_id, shop__pk=shop_id).url
    
def do_get_price(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_price' tag take takes exactly two arguments")
    return PriceNode(bits[1], bits[2])

class PriceNode(template.Node):
    def __init__(self, product_id, shop_id):
        self.product_id = template.Variable(product_id)
        self.shop_id = template.Variable(shop_id)
    def render(self, context):
        product_id = self.product_id.resolve(context)
        shop_id = self.shop_id.resolve(context)
        return ProductShop.objects.get(product__pk=product_id, shop__pk=shop_id).price
        
def do_search_form(parser, token):
    bits = token.split_contents()
    if len(bits) != 3 or bits[1] != 'as':
        raise template.TemplateSyntaxError("'get_search_form' tag takes exactly two arguments")
    return SearchFormNode(bits[2])

class SearchFormNode(template.Node):
    def __init__(self, variable):
        self.variable = variable
    def render(self, context):
        context[self.variable] = SearchForm(auto_id=True)
        return ''
    
register = template.Library()

# syntax: get_login_link
register.tag('show_login_link', do_login_link)

# syntax: get_latest_products <number> from [<application.model> <model_item_id> | all] as <variable>
register.tag('get_latest_products', do_latest_products)

# syntax: get_random_featured_products <number> from [<application.model> <model_item_id> | all] as <variable>
register.tag('get_random_featured_products', do_get_random_featured_products)

# syntax: show_categories_panel
register.tag('show_categories_panel', do_show_categories)

# syntax: get_sorted_shops <product_id> as <variable>
register.tag('get_sorted_shops', do_get_sorted_shops)

# syntax: get_url <product_id> <shop_id>
register.tag('get_url', do_get_url)

# syntax: get_price <product_id> <shop_id>
register.tag('get_price', do_get_price)

# syntax: get_search_form as <variable>
register.tag('get_search_form', do_search_form)