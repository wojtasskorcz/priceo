from django.conf import settings

def additional_settings(request):
    return {'SEARCH_DEFAULT_TEXT': settings.SEARCH_DEFAULT_TEXT,
            'COMMENT_DEFAULT_TEXT': settings.COMMENT_DEFAULT_TEXT,
            'LATEST_PRODUCTS_NUMBER': settings.LATEST_PRODUCTS_NUMBER,
            'RECOMMENDED_PRODUCTS_NUMBER': settings.RECOMMENDED_PRODUCTS_NUMBER}