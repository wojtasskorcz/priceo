from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from priceo import settings

RATING_UP = 1
RATING_DOWN = -1
RATING_CHOICES = ((RATING_UP, 'good'),
                  (RATING_DOWN, 'bad'))

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('priceo.views.categories.category_details', args=[str(self.id)])

class Shop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ratings = models.ManyToManyField(User, through='ShopRating', related_name='shop_ratings')
    register_date = models.DateTimeField(auto_now_add=True, editable=False)
    photo = models.ImageField(upload_to='shops', blank=True, null=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('priceo.views.shops.shop_details', args=[str(self.id)])
    def get_user_vote(self, user):
        try:
            vote = ShopRating.objects.get(shop__pk=self.id, user__pk=user.id)
        except ObjectDoesNotExist:
            return None
        return vote
    def get_thumbs_up(self):
        return ShopRating.objects.filter(shop__pk=self.id, rating=RATING_UP).count()
    def get_thumbs_down(self):
        return ShopRating.objects.filter(shop__pk=self.id, rating=RATING_DOWN).count()
    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            return settings.NO_IMAGE_FILE
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.DateTimeField(verbose_name="publication date", auto_now_add=True, editable=False)
    last_change = models.DateTimeField(verbose_name="last change date", auto_now=True, editable=False)
    shops = models.ManyToManyField(Shop, through='ProductShop', related_name='products')
    category = models.ForeignKey(Category, related_name='products')
    ratings = models.ManyToManyField(User, through='ProductRating', related_name='product_ratings', editable=False)
    photo = models.ImageField(upload_to='products', blank=True, null=True)
    featured = models.BooleanField(default=False, blank=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('priceo.views.products.product_details', args=[str(self.id)])
    def lowest_possible_price(self):
        shops = self.shops.all()
        if not shops:
            return "N/A"
        return reduce(lambda x, y: min(x, ProductShop.objects.get(shop__pk=y.id, product__pk=self.id).price), 
                      shops, ProductShop.objects.get(shop__pk=shops[0].id, product__pk=self.id).price)
    def get_user_vote(self, user):
        try:
            vote = ProductRating.objects.get(product__pk=self.id, user__pk=user.id)
        except ObjectDoesNotExist:
            return None
        return vote
    def get_thumbs_up(self):
        return ProductRating.objects.filter(product__pk=self.id, rating=RATING_UP).count()
    def get_thumbs_down(self):
        return ProductRating.objects.filter(product__pk=self.id, rating=RATING_DOWN).count()
    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            return settings.NO_IMAGE_FILE
    
class ProductShop(models.Model):
    product = models.ForeignKey(Product)
    shop = models.ForeignKey(Shop)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    url = models.URLField()
    def __unicode__(self):
        return "%s in %s" % (self.product.name, self.shop.name)
    
class Rating(models.Model):
    user = models.ForeignKey(User, editable=False)
    rating = models.IntegerField(choices=RATING_CHOICES)

class ProductRating(Rating):
    product = models.ForeignKey(Product, editable=False)
    def __unicode__(self):
        return self.get_rating_display()
    
class ShopRating(Rating):
    shop = models.ForeignKey(Shop, editable=False)
    def __unicode__(self):
        return self.get_rating_display()
    
class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_change = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(User, related_name='comments', editable=False)
    
class ProductComment(Comment):
    product = models.ForeignKey(Product, related_name='comments', editable=False)

class ShopComment(Comment):
    shop = models.ForeignKey(Shop, related_name='comments', editable=False)