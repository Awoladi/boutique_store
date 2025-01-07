from products.models import Category

def categories_processor(request):
    """This processor provides all categories to all templates."""
    return {
        'categories': Category.objects.all()
    }
