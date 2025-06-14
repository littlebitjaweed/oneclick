from django.contrib import admin

from app.models import Order, Profile, Event, SellerApplication, AvailableDate

# Register your models here.

admin.site.register(Event)
admin.site.register(AvailableDate)
admin.site.register(Order)


@admin.register(SellerApplication)
class SellerApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'is_approved', 'submitted_at']
    list_filter = ['is_approved']
    actions = ['approve_seller']

    def approve_seller(self, request, queryset):
        for application in queryset:
            if not application.is_approved:
                application.is_approved = True
                application.save()
                self.message_user(request, f"{application.user.username} has been approved as a seller.")
            else:
                self.message_user(request, f"{application.user.username} is already a seller.")
    approve_seller.short_description = "Approve selected applications"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_no', 'is_seller']
    list_filter = ['is_seller']
