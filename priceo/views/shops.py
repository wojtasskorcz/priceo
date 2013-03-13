from priceo.models import Shop, ShopRating, ShopComment
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

def shop_details(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    user_rating = shop.get_user_vote(request.user)
    message = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['comment']
            ShopComment(text=text, author=request.user, shop=shop).save()
            message = "Comment posted."
        else:
            message = "The form was invalid, try again."
    form = CommentForm({'comment': settings.COMMENT_DEFAULT_TEXT}, auto_id=True)
    return render(request, 'shops/shop_details.html', 
                       {'shop': shop,
                        'user_rating': user_rating,
                        'form': form,
                        'message': message})
    
@login_required
def shop_vote(request, shop_id, rating):
    shop = get_object_or_404(Shop, pk=shop_id)
    last_vote = shop.get_user_vote(request.user)
    if last_vote:
        last_vote.rating = rating;
        last_vote.save()
    else:
        ShopRating(user=request.user, shop=shop, rating=rating).save()
    return HttpResponseRedirect(shop.get_absolute_url())