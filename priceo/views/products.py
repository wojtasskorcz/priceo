from priceo.models import Product, ProductRating, ProductComment
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_rating = product.get_user_vote(request.user)
    message = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['comment']
            ProductComment(text=text, author=request.user, product=product).save()
            message = "Comment posted."
        else:
            message = "The form was invalid, try again."
    form = CommentForm({'comment': settings.COMMENT_DEFAULT_TEXT}, auto_id=True)
    return render(request, 'products/product_details.html', 
                       {'product': product,
                        'user_rating': user_rating,
                        'form': form,
                        'message': message})
    
@login_required
def product_vote(request, product_id, rating):
    product = get_object_or_404(Product, pk=product_id)
    last_vote = product.get_user_vote(request.user)
    if last_vote:
        last_vote.rating = rating;
        last_vote.save()
    else:
        ProductRating(user=request.user, product=product, rating=rating).save()
    return HttpResponseRedirect(product.get_absolute_url())