from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', views.UserViewSet, "user")
router.register('userWecons', views.UserWeconViewSet, "userWecon")
router.register('buildings', views.BuildingViewSet, "building")
router.register('tanks', views.TankViewSet, "tank")
router.register('unitTypes', views.UnitTypeViewSet, "unitType")
router.register('units', views.UnitViewSet, "unit")
router.register('tankTypes', views.TankTypeViewSet, "tankType")
router.register('seasons', views.SeasonViewSet, "season")
router.register('shrimpTypes', views.ShrimpTypeViewSet, "shrimpType")
router.register('shrimpStages', views.ShrimpStageViewSet, "shrimpStage")
router.register('tankPlannings', views.TankPlanningViewSet, "tankPlanning")
router.register('tankMonitorings',
                views.TankMonitoringViewSet, "tankMonitoring")
router.register('foods', views.FoodViewSet, "food")
router.register('foodRecipes', views.FoodRecipeViewSet, "foodRecipe")
router.register('foodRecipeTypes',
                views.FoodRecipeTypeViewSet, "foodRecipeType")
router.register('medicines', views.MedicineViewSet, "medicine")
router.register('medicineUsages', views.MedicineUsageViewSet, "medicineUsages")
router.register('medicineRecipes',
                views.MedicineRecipeViewSet, "medicineRecipe")
router.register('medicineRecipeTypes',
                views.MedicineRecipeTypeViewSet, "medicineRecipeType")
router.register('diseases', views.DiseaseViewSet, "disease")
router.register('works', views.WorkViewSet, "work")
router.register('workMonitorings',
                views.WorkMonitoringViewSet, "workMonitoring")
router.register('careSchedules', views.CareScheduleViewSet, "careSchedule")
router.register('cares', views.CareViewSet, "care")
router.register('reportMonitors', views.ReportMonitorViewSet, 'reportMonitor')
router.register('resultPlans', views.ResultPlanViewSet, 'resultPlan')
router.register('areas', views.AreaViewSet, "area")


urlpatterns = [
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauth2_info/', views.AuthInfo.as_view()),
    path('api/login/', views.login_api),
    path('api/user/', views.get_user_data)
]
