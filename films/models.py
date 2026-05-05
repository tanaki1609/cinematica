from django.db import models


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Film(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE,
                                 null=True)  # director_id
    genres = models.ManyToManyField(Genre, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.FloatField()
    is_hit = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def genre_names(self):
        return [i.name for i in self.genres.all()]


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=((i, '* ' * i) for i in range(1, 11)))
    film = models.ForeignKey(Film, on_delete=models.CASCADE,
                             related_name='reviews')  # film_id

    def __str__(self):
        return self.text
