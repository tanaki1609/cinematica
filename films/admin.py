from django.contrib import admin
from .models import Film, Genre, Director, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class FilmAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = 'title director rating_kp created updated'.split()
    search_fields = 'title text'.split()
    list_filter = 'director genres'.split()


admin.site.register(Film, FilmAdmin)
admin.site.register(Director)
admin.site.register(Genre)
