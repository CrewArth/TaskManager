
from django.contrib import admin
from django.urls import path
from Workspace.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name= "homepage"),
    path('add_task/', add_task, name="add_task"),
    path('delete/<int:id>/', delete, name="deletetask"),
    path('update/<int:id>/', update, name="updatetask"),
    path('login/', login_page, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout_page, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)