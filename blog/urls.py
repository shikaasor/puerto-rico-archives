from django.urls import path
from .views import (
    fileListView,
    fileDetailView,
    fileCreateView,
    fileUpdateView,
    fileDeleteView,
    UserfileListView
)
from . import views

urlpatterns = [
    path('', fileListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserfileListView.as_view(), name='user-files'),
    path('file/<int:pk>/', fileDetailView.as_view(), name='file-detail'),
    path('file/new/', fileCreateView.as_view(), name='file-create'),
    path('file/<int:pk>/update/', fileUpdateView.as_view(), name='file-update'),
    path('file/<int:pk>/delete/', fileDeleteView.as_view(), name='file-delete'),
    path('media/Files/<int:pk>',fileDeleteView.as_view(),name='file-delete' ),
    path('search/',views.search,name='search' ),
    path('about/', views.about, name='blog-about'),
]
