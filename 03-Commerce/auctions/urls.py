from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # MY ADDS:
    path("newproduct", views.new_product, name="newproduct"),
    path("product_<int:product_id>", views.product_view, name="product"),
    path("newbid_<int:product_id>", views.new_bid, name="newbid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("delete_<int:product_id>", views.delete, name="delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
