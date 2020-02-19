from django.contrib import admin

from .models import Lecture, Prof, SimilarLecture, SimilarProf, Icon
# Register your models here.
admin.site.register(Lecture)
admin.site.register(Prof)
admin.site.register(SimilarLecture)
admin.site.register(SimilarProf)
admin.site.register(Icon)
