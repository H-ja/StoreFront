from django.contrib import admin, messages
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1

    # showing a thumnail of image
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html('<img src="{}", class="thumbnail" />', instance.image.url)
        # adding some CSS features in static folder of store app
        # NOTE: django automatically looks for this folder
        return ''


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title', 'description']
    }
    autocomplete_fields = ['collection']
    search_fields = ['title']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    inlines = [ProductImageInline]

    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'High'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated",
            messages.SUCCESS
            )

    # defining a class called < Media (NOTE: name is important exactly like Meta class) >
    # we can tell django to look for our static assets
    class Media:
        css = {
            # in css we have ['screen', 'print', 'all']
            'all': ['store/styles.css']
            # NOTE: we are not using static/ because django is automatically looking inside this folder in Media class
            # --> static/ path is defined in settings.py
        }
    # NOTE: using a sub folder like store/ because django will automatically look for static folders
    # and there could be a lot of styles.css files so we would get error!


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') 
        + '?'
        + urlencode({'collection_id': collection.id})
        )
        return format_html('<a href={}>{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_select_related = ['user']
    list_display = ['user__first_name', 'user__last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']
    # me
    autocomplete_fields = ['user']

    @admin.display(ordering='orders')
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist')
        + '?'
        + urlencode({'customer__id': str(customer.id)}))
        return format_html('<a href={}>{}</a>', url, customer.orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders=Count('order')
        )


class OrderItemInLine(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 1
    max_num = 5


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10
    ordering = ['customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInLine]
