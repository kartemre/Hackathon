from django.contrib import admin
from .models import User, WaterUsage, Award

# User modelini sadece bir kez kaydet
try:
    admin.site.register(User)
except admin.sites.AlreadyRegistered:
    pass

# WaterUsage modeli ve admin konfigürasyonu
class WaterUsageAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'user', 'billing_month', 'billing_year', 'is_recent')
    search_fields = ('user__tc', 'barcode', 'billing_month', 'billing_year')
    list_filter = ('billing_month', 'billing_year', 'is_recent')
    actions = ['mark_as_recent', 'mark_as_not_recent']

    def mark_as_recent(self, request, queryset):
        queryset.update(is_recent=True)
    mark_as_recent.short_description = 'Seçilen faturaları en güncel olarak işaretle'

    def mark_as_not_recent(self, request, queryset):
        queryset.update(is_recent=False)
    mark_as_not_recent.short_description = 'Seçilen faturaları en güncel değil olarak işaretle'

# Award modeli ve admin konfigürasyonu
class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'month', 'year', 'is_recent')
    search_fields = ('name', 'category', 'month', 'year')
    list_filter = ('month', 'year', 'is_recent', 'category')
    actions = ['mark_as_recent', 'mark_as_not_recent']

    def mark_as_recent(self, request, queryset):
        queryset.update(is_recent=True)
    mark_as_recent.short_description = 'Seçilen ödülleri en güncel olarak işaretle'

    def mark_as_not_recent(self, request, queryset):
        queryset.update(is_recent=False)
    mark_as_not_recent.short_description = 'Seçilen ödülleri en güncel değil olarak işaretle'

# WaterUsage ve Award modellerini kaydet
try:
    admin.site.register(WaterUsage, WaterUsageAdmin)
    admin.site.register(Award, AwardAdmin)
except admin.sites.AlreadyRegistered:
    pass