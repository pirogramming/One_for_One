from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('new/<int:pk>/', views.match_new, name='match_new'),
    path('cat/<int:pk>/', views.choice_cat, name='choice_cat'),
    path('cat/<int:pk>/store/', views.choice_store, name='choice_store'),
    path('new/fin/', views.match_fin, name='match_fin'),
    path('mypage/', views.mypage, name='mypage'),
]