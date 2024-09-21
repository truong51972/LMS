from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import Quiz_Form
from .models import Course, Quiz

from django.core.cache import cache

