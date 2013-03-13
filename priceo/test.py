from priceo.models import Category, Shop, Product, ProductShop

def test():
    c = [Category(name='Laptops'), Category(name='Smartphones'), Category(name='Bicycles'), Category(name='Shoes')]
    for category in c:
        category.save()
    
    s = [Shop(name='x-kom.pl'), Shop(name='laptopy.pl'), Shop(name='netbooks.com')]
    s.extend([Shop(name='telepolis.pl'), Shop(name='mobilne.pl'), Shop(name='smartfony.pl'), Shop(name='komorki.pl')])
    s.extend([Shop(name='rowery.pl'), Shop(name='plbike.pl'), Shop(name='rowerowo.pl')])
    s.extend([Shop(name='sneakers.com'), Shop(name='buty.pl'), Shop(name='trzewiki.pl')])
    for shop in s:
        shop.save()
    
    p = [Product(name='Asus EeePC', description='Eee PC 1011CX N2600/1GB/320 bialy', category=c[0], featured=True)]
    p.append(Product(name='Acer AOD270', description='AOD270 N2600/1GB/320/7SE 6CELL czarny', category=c[0], featured=True))
    p.append(Product(name='Dell Vostro 3460', description='Vostro 3460 i3-2328M/4GB/500/DVD-RW srebrny', category=c[0]))
    p.append(Product(name='Fujitsu S752', description='S752 i3-3110M/4GB/500/DVD-RW/Win8P', category=c[0], featured=True))
    p.append(Product(name='HP EliteBook 8470p', description='EliteBook 8470p i7-3520M/4GB/500/DVD-RW/7Pro64', category=c[0]))
    p.append(Product(name='Lenovo Edge E430', description='Edge E430 i5-3210M/4GB/500/DVD-RW/7HP64', category=c[0], featured=True))
    p.append(Product(name='Lenovo ThinkPad T430u', description='ThinkPad T430u i7-3517U/8GB/1000/7Pro64', category=c[0]))
    p.append(Product(name='Lenovo ThinkPad X1', description='ThinkPad X1 Carbon i5-3427U/4GB/256/Win8P', category=c[0]))
    p.append(Product(description='G585G E1-1200M/4GB/500/DVD-RW HD7310', name='Lenovo G585G', category=c[0], featured=True))
    p.append(Product(description='ThinkPad L530 B970/4GB/500/DVD-RW', name='Lenovo ThinkPad L530', category=c[0]))
    p.append(Product(description='Inspiron 5720 i5-3210M/16GB/500/DVD-RW', name='Dell Inspiron 5720', category=c[0]))
    p.append(Product(description='G780A i3-3110M/4GB/1000/DVD-RW/Win8 GT635M', name='Lenovo G780A', category=c[0], featured=True))
    p.append(Product(description='GE70 0ND i5-3210M/12GB/750/DVD-RW FHD GTX660', name='MSI GE70', category=c[0], featured=True))
    for product in p:
        product.save()
        
    p.reverse()
    ps = [ProductShop(product=p[0], shop=s[0], price=1500, url="http://www.wp.pl")]
    ps.append(ProductShop(product=p[0], shop=s[1], price=1600, url="http://www.wp.pl"))
    ps.append(ProductShop(product=p[0], shop=s[2], price=1400, url="http://www.wp.pl"))
    ps.append(ProductShop(product=p[1], shop=s[0], price=1800, url="http://www.wp.pl"))
    ps.append(ProductShop(product=p[1], shop=s[1], price=1700, url='http://www.wp.pl'))
    ps.append(ProductShop(product=p[1], shop=s[2], price=2000, url='http://www.wp.pl'))
    for product_shop in ps:
        product_shop.save()