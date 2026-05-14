from django.contrib import admin
from .models import Route, SiteVisit

class SiteVisitInline(admin.TabularInline):
    model = SiteVisit
    extra = 1

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = [SiteVisitInline]

admin.site.register(SiteVisit)
