"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    
    path('register/',views.Register, name='register'),
    path('login/',views.Login,name='login'),
    path('adminhome/',views.adminhomecall,name='adminhome'),
    path('userhome/', views.userhomecall, name='userhome'),

    path('category/',views.Add_category,name='category'),
    path('catdelete/<int:id>',views.Catdelete,name="catdelete"),
    path('catedit/<int:id>',views.Catedit,name="catedit"),

    path('users/',views.User_management,name="users"),
    path('userdelete/<int:id>/', views.Userdelete, name='userdelete'),

    path('expense/',views.Add_expense,name='expense'),
    path('exdelete/<int:id>',views.Exdelete,name="exdelete"),
    path('exedit/<int:id>',views.Exedit,name="exedit"),

    path('catrack/',views.Categorized_tracking,name='catrack'),
    
    path('report/',views.report_page,name='report'),

    path('groups/', views.Groups, name='groups'),
    path('group/<int:id>/', views.Group_detail, name='group_detail'),
    path('notifications/', views.notifications, name='notifications'),


    path('logout/', views.Logout, name='logout'),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
