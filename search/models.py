from django.db import models

import json
import ast  # list 만들어주기
from django.core import serializers
from django.forms.models import model_to_dict
import re
# Create your models here.


class LectureManager(models.Manager):

    def get_by_natural_key(self, name, prof_name):
        return self.get(name=name, prof_name=prof_name)


# name, class_code, score, category, prof, time, recommend_year, weight, competitor, remarks, link, semester
class Lecture(models.Model):
    name = models.CharField(max_length=100)
    # 교수랑 외래키 설정 교수이름 가져오는거
    prof = models.ForeignKey(
        'Prof', blank=True, related_name="lectures", on_delete=models.CASCADE)
    prof_name = models.CharField(max_length=100, default='승호')
    class_type = models.CharField(max_length=100)
    class_code = models.CharField(max_length=20)
    score = models.CharField(max_length=10)
    category = models.CharField(max_length=100)
    time = models.CharField(max_length=500)
    recommend_year = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    semester = models.CharField(max_length=255)
    hash_tags = models.CharField(max_length=300, default="['해쉬', '스완', '창모']")
    attendance = models.CharField(max_length=100, null=True)
    score_stlict = models.CharField(max_length=100, null=True)
    homework = models.CharField(max_length=100, null=True)
    teamplay = models.CharField(max_length=100, null=True)
    test_time = models.CharField(max_length=100, null=True)
    positive = models.CharField(max_length=100, null=True)
    negative = models.CharField(max_length=100, null=True)
    # 유사강의들 similarlecture에서 가져옴
    similar_lectures = models.ManyToManyField("self", blank=True, related_name="+", through="SimilarLecture",
                                              symmetrical=False)
    # Icon 모델이랑 연결
    icon = models.ForeignKey('Icon', null=True, related_name="l_icons", on_delete=models.SET_NULL)

    objects = LectureManager()

    class Meta:
        # Lectures' name, prof can be same, but time must not be same.
        unique_together = ("name", "prof", "time")

    def natural_key(self):
        # self.prof_name = self.prof.name # 없어도됨... 나중에 까먹지 않기위함
        return (self.name, self.prof.name,)

    natural_key.dependencies = ['search.prof']

    @property
    def get_hash_tags(self):
        return ast.literal_eval(self.hash_tags)

    @property
    def get_category(self):
        return self.category

    @property
    def get_semester(self):
        return self.semester[1:-1]

    @property
    def get_class_type(self):
        return self.class_type[1:-1]

    @property
    def get_score(self):
        return round(float(self.score), 2)

    @property
    def get_positive(self):
        return round(float(self.positive), 2)

    @property
    def get_negative(self):
        return round(float(self.negative), 2)

    @property
    def get_time(self):
        time = re.sub('<br>', ', ', self.time)
        return time

    @property
    def get_star(self):
        star_count = int(float(self.score) // 1)
        return {
            'full_star': range(star_count),
            'half_star': float(self.score) - star_count
        }


class SimilarLecture(models.Model):
    """
    me           => others
    similar_from => similar_to
                 => similar_to
    """
    similar_from = models.ForeignKey(
        Lecture, blank=True, null=True, on_delete=models.CASCADE, related_name="similar_from")
    similar_to = models.ForeignKey(
        Lecture, blank=True, null=True, on_delete=models.CASCADE, related_name="similar_to")

# 교수 테이블
class ProfManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Prof(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    category = models.CharField(max_length=100)
    hash_tags = models.CharField(max_length=300)
    attendance = models.CharField(max_length=300)
    score = models.CharField(max_length=100, null=True)
    score_stlict = models.CharField(max_length=300)
    homework = models.CharField(max_length=300)
    teamplay = models.CharField(max_length=300)
    test_time = models.CharField(max_length=300)
    positive = models.CharField(max_length=100, null=True)
    negative = models.CharField(max_length=100, null=True)

    # 유사교수들은 many to many로
    similar_profs = models.ManyToManyField("self", blank=True, related_name="+", through="SimilarProf",
                                           symmetrical=False)
    # Icon 모델이랑 연결
    icon = models.ForeignKey('Icon', null=True, related_name="p_icons", on_delete=models.SET_NULL)

    objects = ProfManager()

    def natural_key(self):
        return (self.name,)

    def get_hash_tags(self):
        return ast.literal_eval(self.hash_tags)

    def get_category(self):
        return self.category

    def get_score(self):
        return round(float(self.score), 2)

    def get_positive(self):
        return round(float(self.positive), 2)

    def get_negative(self):
        return round(float(self.negative), 2)

    def get_star(self):
        star_count = int(float(self.score) // 1)
        return {
            'full_star': range(star_count),
            'half_star': float(self.score) - star_count
        }


class SimilarProf(models.Model):
    """
    me           => others
    similar_from => similar_to
                 => similar_to
    """
    # from to로 교수의 정보를 가져올 수 있게 유사ㅑㅐ
    similar_from = models.ForeignKey(
        Prof, blank=True, null=True, on_delete=models.CASCADE, related_name="similar_from")
    similar_to = models.ForeignKey(
        Prof, blank=True, null=True, on_delete=models.CASCADE, related_name="similar_to")


class IconManager(models.Manager):
    def get_by_natural_key(self, category):
        return self.get(category=category)

class Icon(models.Model):
    category = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    
    objects = IconManager()

    def natural_key(self):
        return (self.category,)