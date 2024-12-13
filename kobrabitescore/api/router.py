from django.conf import settings
from rest_framework_nested import routers

import user.views
import client.views

router = routers.DefaultRouter()
router.register(r"users", user.views.UserViewSet)
router.register(r"register", user.views.RegisterViewSet, basename="register")
router.register(r"login", user.views.LoginViewSet, basename="login")
router.register(r"logout", user.views.LogoutViewSet, basename="logout")
