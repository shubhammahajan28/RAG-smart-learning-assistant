from django.urls import path
from .views import RegisterView, LoginView, ImportCSVView, AnalyzeWeaknessView, RAGQueryView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("import_csv/", ImportCSVView.as_view()),
    path("analyze/", AnalyzeWeaknessView.as_view()),
    path("rag/", RAGQueryView.as_view()),
]