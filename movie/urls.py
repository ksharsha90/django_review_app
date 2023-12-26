from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>', views.detail, name='detail'),
    path('<int:movie_id>/create', views.review_create_view,
         name='review_create_view'),
    path('review/<int:review_id>/update', views.review_update_view,
         name='review_update_view'),
    path('review/<int:review_id>/delete', views.review_delete_view,
         name='review_delete_view'),
    path('about/', views.about),
]