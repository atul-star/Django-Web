from django.contrib import admin

# Register your models here.
from .models import Contact
# from django.contrib import admin

# Customize site header and title
admin.site.site_header = 'आर.के फाइनेंशियल'
admin.site.site_title = 'आर.के फाइनेंशियल'

# admin.site.register(Contact)

@admin.register(Contact)
class YourModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]  # Display all fields
    list_filter = ['id','name', 'email','mobile']  # Add filtering options for field1 and field2
    search_fields = ['name']  # Enable searching within field1 and field2
