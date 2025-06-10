from django.contrib import admin
from django.urls import path,include
from index.views import FormAPI,QuestionAPI,ChoiceAPI
urlpatterns = [
   path('form/',FormAPI.as_view()),
   path('question/',QuestionAPI.as_view()),
   path('choices/',ChoiceAPI.as_view()),
] 