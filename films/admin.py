from django.contrib import admin
from .models import Film, Director, Genre, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class FilmAdmin(admin.ModelAdmin):
    list_filter = 'director genres'.split()
    search_fields = 'title text'.split()
    list_display = 'title is_hit director created'.split()
    inlines = [ReviewInline]


admin.site.register(Film, FilmAdmin)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Review)
