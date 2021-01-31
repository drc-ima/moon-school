"""school_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.account.views import user_login
from apps.school import urls as school_urls
from apps.account import urls as account_urls
from apps.staff import urls as staff_urls
from apps.pupil import urls as pupil_urls
from apps.schedule import urls as schedule_urls
from apps.finance import urls as finance_urls
api_paths = [
    # path('school/', include(school_urls, namespace='school'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_paths)),
    path('', user_login, name='login'),
    path('school/', include(school_urls, namespace='school')),
    path('account/', include(account_urls, namespace='account')),
    path('finance/', include(finance_urls, namespace='finance')),
    path('staff/', include(staff_urls, namespace='staff')),
    path('pupil/', include(pupil_urls, namespace='pupil')),
    path('schedule/', include(schedule_urls, namespace='schedule')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
