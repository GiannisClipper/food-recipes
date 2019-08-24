from django.urls import path

from user import views

app_name = 'user'
# help identifying app when url created with reverse
# for example: reverse('user:create')

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
