from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path(
        "datasource/",
        views.DatasourceList.as_view(),
        name="datasource-list",
    ),
    path(
        "datasource/<int:pk>/",
        views.DatasourceDetail.as_view(),
        name="datasource-detail",
    ),
    path(
        "content-pool/",
        views.ContentPoolListView.as_view(),
        name="content-pool-list",
    ),
    path(
        "content-pool/<int:pk>/",
        views.ContentPoolDetailView.as_view(),
        name="content-pool-detail",
    ),
    path(
        "ingested-text-content/",
        views.InjestedTextContentListView.as_view(),
        name="ingested-text-content-list",
    ),
    path(
        "ingested-text-content/<int:pk>/",
        views.InjestedTextContentDetailView.as_view(),
        name="ingested-text-content-detail",
    ),
    path(
        "extracter-chain/",
        views.ExtracterChainListView.as_view(),
        name="extracter-chain-list",
    ),
    path(
        "extracter-chain/<int:pk>/",
        views.ExtracterChainDetailView.as_view(),
        name="extracter-chain-detail",
    ),
    path(
        "extracter-prompt/",
        views.ExtracterPromptListView.as_view(),
        name="extracter-prompt-list",
    ),
    path(
        "extracter-prompt/<int:pk>/",
        views.ExtracterPromptDetailView.as_view(),
        name="extracter-prompt-detail",
    ),
    path(
        "processed-data/",
        views.ProcessedDataListView.as_view(),
        name="processed-data-list",
    ),
    path("login/", views.LoginView.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]
