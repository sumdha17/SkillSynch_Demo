from rest_framework.routers import DefaultRouter
from api.v1.views import question_view, user_view, course_view, module_view, lesson_view, assignee_view, answers_view, userscore_view, useranswer_view
from django.urls import include, path
from api.v1.views.course_category_view import CategoryViewSet


# Create a router and register our ViewSet
router = DefaultRouter()

router.register(r'user', user_view.UserGetUpdateViewSet, basename='user')
router.register(r'all-user', user_view.GetAllUserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'courses', course_view.CourseViewSet)
router.register(r'modules', module_view.ModuleViewSet)
router.register(r'lessons', lesson_view.LessonViewSet)
router.register(r'questions', question_view.QuestionViewSet)
router.register(r'answers', answers_view.AnswerViewSet)
router.register(r'assignees', assignee_view.AssigneeViewSet)
router.register(r'user-score', userscore_view.UserScoreViewSet)
router.register(r'user-answer', useranswer_view.UserAnswerViewSet)



urlpatterns = [
    path("signup/", user_view.SignUpAPIView.as_view(), name="signup"),
    path("login/", user_view.LoginAPIView.as_view(), name="login"),
    path("logout/", user_view.LogoutAPIView.as_view(), name="logout"),
    path("forgot-password/",user_view.ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/<str:token>/",user_view.ResetPasswordAPIView.as_view(), name="reset-password"),
    path("user-me/", user_view.MeAPIView.as_view(), name="user-me"),
    path('', include(router.urls))
    
]