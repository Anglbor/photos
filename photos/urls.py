"""photos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from photo_app.views import DisplayView, Photo_upload_view, LoginView, LogoutView, PhotoView, SearchView, delete_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('display/', DisplayView.as_view(), name="display"),
    path('upload/', Photo_upload_view.as_view(), name='upload'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('photo/<int:id>/', PhotoView.as_view(), name='photo'),
    path('search/', SearchView.as_view(), name='search'),
    # path('logout', LogoutView.as_view())
    path('delete/<int:id>/', delete_view, name='delete')
]



if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)