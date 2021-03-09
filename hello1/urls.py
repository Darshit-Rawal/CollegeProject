from django.urls import path
from hello1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("", views.login, name="login"),
    #path("graph", views.getimage, name="getimage"),
    path('home',views.home,name="home"),
    #path('dashboard',views.dashboard,name="dashboard"),
    path('userdata',views.loginDatabase,name="loginDatabase"),
    path('postRegistration',views.postRegistration,name="postRegistration"),
    path('postlogin',views.postlogin,name="postlogin"),
    path('imageupload',views.upload,name="imageupload"),
    path('getimage', views.getimage, name="getimage"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('postdashboard', views.postdashboard, name="postdashboard"),
    path('postearthengine', views.postearthengine, name="postearthengine"),
    path('earthengine', views.earthengine, name="earthengine"),
    path('forestApproximation', views.forestApproximation, name="forestApproximation"),
    path('visulizeForest', views.visulizeForest, name="visulizeForest"),
    path('forestfire', views.forestfire, name="forestfire"),
    path('postforestfire', views.postforestfire, name="postforestfire"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
