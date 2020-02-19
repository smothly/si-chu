# search/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
import json
import re
from collections import Counter
import random

from .models import Lecture, SimilarLecture, Prof, SimilarProf, Icon

# logger
import urllib
from google.cloud import logging

logging_client = logging.Client()
log_name = 'sichu-log'
logger = logging_client.logger(log_name)

# 메인페이지
User = get_user_model()


# 메인페이지

def index(request):
    now = datetime.now()
    context = {
        'search_bar': False
    }
    return render(request, 'search/index.html', context)


# 검색결과 페이지: 4개 정보 - 2개 섹션 표시

@login_required
def search(request):
    origin_keyword = request.GET['keyword']
    # 키워드 숫자 한글 영어만 정규표현식으로 남기고 공백기준 스플릿
    keyword = re.sub('[^0-9a-zA-Zㄱ-힗\s]', '', origin_keyword)
    keyword = keyword.split(' ')

    '''
    특정한 강의 찾기
    ex) 네트워크, 이상환, 월 A
    '''
    show_lectures = []
    lectures = []
    # 4가지 필드에서 가장 많이뽑힌 것들이 우선순위
    for k in keyword:
        # 강의 제목 / 학부 / 시간&장소 / 교수 / 학기 이름으로 뽑기
        lectures_1 = list(Lecture.objects.filter(name__icontains=k))  # 강의제목
        lectures_2 = list(Lecture.objects.filter(category__icontains=k))  # 학부
        lectures_3 = list(Lecture.objects.filter(time__icontains=k))  # 시간 & 장소
        lectures_4 = list(Lecture.objects.filter(prof_name__icontains=k))  # 교수
        lectures_5 = list(Lecture.objects.filter(hash_tags__icontains=k)) # 해쉬태그

        lectures += lectures_1 + lectures_2 + lectures_3 + \
                    lectures_4 + lectures_5

    distinct_lectures = list(set(lectures))

    for lec in distinct_lectures:
        if str(lec.hash_tags) != "['정보없음']":
            lectures.append(lec)
        if '2020-1' in lec.semester:
            lectures.append(lec)
    
    lectures = Counter(lectures).most_common()[:20]  # 상위 카운트 20개
    
    lectures = [lec[0] for lec in lectures]


    show_lectures = lectures
    # print('키워드 강의 개수', len(lectures))


    '''
    키워드 교수 찾기
    '''
    show_profs = []
    profs = []
    # 2가지 필드에서 가장 많이뽑힌 것들이 우선순위
    for k in keyword:
        # 교수이름 / 학부 뽑기
        profs_1 = list(Prof.objects.filter(name__icontains=k))  # 교수이름
        profs_2 = list(Prof.objects.filter(category__icontains=k))  # 학부
        profs_3 = list(Prof.objects.filter(hash_tags__icontains=k))

        profs += profs_1 + profs_2 + profs_3

    profs = Counter(profs).most_common()[:10]  # 상위 카운트 10개
    profs = [p[0] for p in profs]
    # print('키워드 교수 개수', len(profs))

    show_profs += profs

    users = User.objects.prefetch_related('favorite_lectures')
    user = users.get(pk=request.user.pk)

    context = {
        'message': str(keyword)[1:-1] + '를 검색하셨습니다.',
        'lecture': show_lectures,
        'prof': show_profs,
        'uesr': user,
        'keywords': origin_keyword,
    }

    logger.log_struct({
            'user' : str(user),
            'from' : urllib.parse.unquote(request.META.get('HTTP_REFERER')),
            'key' : keyword,
            'type' : 'search'})  

    return render(request, 'search/search.html', context)


# 강의 상세페이지
@login_required
def lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    similar_relationship = SimilarLecture.objects.filter(
        similar_from=lecture_id)
    similar_lectures = Lecture.objects.filter(id=999999)  # 빈 쿼리셋
    # 유사강의들 쿼리셋에 담기
    for sim_rel in similar_relationship:
        similar_lectures = similar_lectures | Lecture.objects.filter(
            id=sim_rel.similar_to.id)

    context = {
        'lecture': lecture,
        'similar_lectures': similar_lectures
    }

    logger.log_struct({
            'user' : str(request.user.username),
            'from' : urllib.parse.unquote(request.META.get('HTTP_REFERER')),
            'key_specific_name' : lecture.name,
            'key' : lecture_id,
            'type' : 'lecture'})  

    return render(request, 'search/lecture.html', context)


# 교수 상세페이지
@login_required
def prof(request, prof_id):
    prof = get_object_or_404(Prof, pk=prof_id)
    similar_relationship = SimilarProf.objects.filter(similar_from=prof_id)
    similar_profs = Prof.objects.filter(id=999999)  # 빈 쿼리셋

    # 유사강의들 쿼리셋에 담기
    for sim_rel in similar_relationship:
        similar_profs = similar_profs | Prof.objects.filter(
            id=sim_rel.similar_to.id)

    # 이번학기 열린강의
    lecture_list_1 = Lecture.objects.filter(prof_name=prof.name)
    lecture_list_2 = Lecture.objects.filter(semester__icontains='2020-1')

    lecture_list = lecture_list_1 & lecture_list_2

    context = {
        'prof': prof,
        'similar_profs': similar_profs,
        'lecture_list': lecture_list
    }

    logger.log_struct({
            'user' : str(request.user.username),
            'from' : urllib.parse.unquote(request.META.get('HTTP_REFERER')),
            'key_specific_name' : prof.name,
            'key' : prof_id,
            'type' : 'prof'})  

    return render(request, 'search/prof.html', context)


# global variables


def colors(request):
    c = ['red', 'blue', 'yellow']
    return {
        'colors': random.sample(c, 1)
    }
