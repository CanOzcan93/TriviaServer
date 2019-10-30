from django.contrib import admin
from example.models import Person, Game, Membership

# Register your models here.
admin.site.register(Person)
admin.site.register(Game)
admin.site.register(Membership)

