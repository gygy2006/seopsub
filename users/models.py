from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    """ Custom User Model """

    GANDER_MALE = "male"
    GANDER_FEMALE = "female"
    GANDER_CHOICES = ((GANDER_MALE, "Male"), (GANDER_FEMALE, "Female"))

    RESIDENCE_SEOUL = "seoul"
    RESIDENCE_INCHEON = "incheon"
    RESIDENCE_GYEONGGI = "gyeonggi"
    RESIDENCE_GANGWON = "gangwon"
    RESIDENCE_CHUNGBUK = "chungbuk"
    RESIDENCE_CHUNGNAM = "chungnam"
    RESIDENCE_GYEONGNAM = "gyeongnam"
    RESIDENCE_GYEONGBUK = "gyeongbuk"
    RESIDENCE_JEONBUK = "jeonbuk"
    RESIDENCE_JEONNAM = "jeonnam"
    RESIDENCE_JEJU = "jeju"
    RESIDENCE_OTHER = "other"

    RESIDENCE_CHOICES = (
        (RESIDENCE_SEOUL, "서울"),
        (RESIDENCE_INCHEON, "인천"),
        (RESIDENCE_GYEONGGI, "경기도"),
        (RESIDENCE_GANGWON, "강원도"),
        (RESIDENCE_CHUNGBUK, "충청북도"),
        (RESIDENCE_CHUNGNAM, "충청남도"),
        (RESIDENCE_GYEONGBUK, "경상북도"),
        (RESIDENCE_GYEONGNAM, "경상남도"),
        (RESIDENCE_JEONBUK, "전라북도"),
        (RESIDENCE_JEONNAM, "전라남도"),
        (RESIDENCE_JEJU, "제주도"),
        (RESIDENCE_OTHER, "그외"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GANDER_CHOICES, max_length=10, blank=True)
    residence = models.CharField(choices=RESIDENCE_CHOICES, max_length=10, blank=True)
    introduction = models.TextField(blank=True)
