
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, permissions, status, generics
from .models import (Building, BuildingType, Care, CareSchedule, Disease, Food, FoodRecipe, FoodRecipeType, Medicine, MedicineRecipe, MedicineRecipeType, MedicineUsage, Season, ShrimpStage, ShrimpType, Tank, TankMonitoring, TankPlanning, TankType,
                     Unit, UnitType, User, UserWecon, Work, WorkMonitoring)
from .serializers import (
    BuildingSerializer,
    BuildingTypeSerializer,
    CareScheduleSerializer,
    CareSerializer,
    DiseaseSerializer,
    FoodRecipeSerializer,
    FoodRecipeTypeSerializer,
    FoodSerializer,
    MedicineRecipeSerializer,
    MedicineRecipeTypeSerializer,
    MedicineSerializer,
    MedicineUsageSerializer,
    SeasonSerializer,
    ShrimpStageSerializer,
    ShrimpTypeSerializer,
    TankMonitoringSerializer,
    TankPlanningSerializer,
    TankSerializer,
    TankTypeSerializer,
    UnitSerializer,
    UnitTypeSerializer,
    UserSerializer,
    UserWeconSerializer,
    WorkMonitoringSerializer,
    WorkSerializer)
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken


@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)

    device_token = request.data.get('device_token')
    if device_token is not None:
        user.device_token = device_token
        user.save()
    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'device_token': user.device_token,
            'user_wecon': user.user_wecon_id,
            'first_name': user.first_name,
            'last_name': user.last_name
        },
        'token': token
    })


@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user is not None:
        return Response(data={'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }})
    return Response(data={'error': 'not authenticated'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(seft, request):
        return Response(seft.serializer_class(request.user).data, status=status.HTTP_200_OK)

    def list(self, request):
        users = User.objects.filter(is_active=True)

        serializer = UserSerializer(users, many=True)
        return Response(data={"users": serializer.data}, status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(seft, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class UserWeconViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = UserWecon.objects.filter(active=True)
    serializer_class = UserWeconSerializer


class BuildingTypeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = BuildingType.objects.filter(active=True)
    serializer_class = BuildingTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        buildingTypes = BuildingType.objects.filter(active=True)

        serializer = BuildingTypeSerializer(buildingTypes, many=True)
        return Response(data={"buildingTypes": serializer.data}, status=status.HTTP_200_OK)


class BuildingViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Building.objects.filter(active=True)
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        buildings = Building.objects.filter(active=True)
        building_type = request.query_params.get('building_type')
        if building_type is not None:
            buildings = buildings.filter(building_type=building_type)

        serializer = BuildingSerializer(buildings, many=True)
        return Response(data={"buildings": serializer.data}, status=status.HTTP_200_OK)


class UnitTypeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = UnitType.objects.filter(active=True)
    serializer_class = UnitTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        unitTypes = UnitType.objects.filter(active=True)

        serializer = UnitTypeSerializer(unitTypes, many=True)
        return Response(data={"unitTypes": serializer.data}, status=status.HTTP_200_OK)


class UnitViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Unit.objects.filter(active=True)
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        units = Unit.objects.filter(active=True)
        unit_type = request.query_params.get('unit_type')
        if unit_type is not None:
            units = units.filter(unit_type=unit_type)

        serializer = UnitSerializer(units, many=True)
        return Response(data={"units": serializer.data}, status=status.HTTP_200_OK)


class TankViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Tank.objects.filter(active=True)
    serializer_class = TankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tanks = Tank.objects.filter(active=True)
        building = request.query_params.get('building')
        if building is not None:
            tanks = tanks.filter(building=building)

        serializer = TankSerializer(tanks, many=True)
        return Response(data={"tanks": serializer.data}, status=status.HTTP_200_OK)


class TankTypeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = TankType.objects.filter(active=True)
    serializer_class = TankTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tankTypes = TankType.objects.filter(active=True)

        serializer = TankTypeSerializer(tankTypes, many=True)
        return Response(data={"tankTypes": serializer.data}, status=status.HTTP_200_OK)


class SeasonViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Season.objects.filter(active=True)
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        seasons = Season.objects.filter(active=True)

        serializer = SeasonSerializer(seasons, many=True)
        return Response(data={"seasons": serializer.data}, status=status.HTTP_200_OK)


class ShrimpTypeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = ShrimpType.objects.filter(active=True)
    serializer_class = ShrimpTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        shrimpTypes = ShrimpType.objects.filter(active=True)

        serializer = ShrimpTypeSerializer(shrimpTypes, many=True)
        return Response(data={"shrimpTypes": serializer.data}, status=status.HTTP_200_OK)


class ShrimpStageViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = ShrimpStage.objects.filter(active=True)
    serializer_class = ShrimpStageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        shrimpStages = ShrimpStage.objects.filter(active=True)
        shrimp_type = request.query_params.get('shrimp_type')
        if shrimp_type is not None:
            shrimpStages = shrimpStages.filter(shrimp_type=shrimp_type)

        serializer = ShrimpStageSerializer(shrimpStages, many=True)
        return Response(data={"shrimpStages": serializer.data}, status=status.HTTP_200_OK)


class TankPlanningViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = TankPlanning.objects.filter(active=True)
    serializer_class = TankPlanningSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tankPlans = TankPlanning.objects.filter(active=True)
        season = request.query_params.get('season')
        if season is not None:
            tankPlans = tankPlans.filter(season=season)
        tank = request.query_params.get('tank')
        if tank is not None:
            tankPlans = tankPlans.filter(tank=tank)

        serializer = TankPlanningSerializer(tankPlans, many=True)
        return Response(data={"tankPlans": serializer.data}, status=status.HTTP_200_OK)


class TankMonitoringViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = TankMonitoring.objects.filter(active=True)
    serializer_class = TankMonitoringSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tankMonitors = TankMonitoring.objects.filter(active=True)

        serializer = TankMonitoringSerializer(tankMonitors, many=True)
        return Response(data={"tankMonitors": serializer.data}, status=status.HTTP_200_OK)


class FoodViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Food.objects.filter(active=True)
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        foods = Food.objects.filter(active=True)

        serializer = FoodSerializer(foods, many=True)
        return Response(data={"foods": serializer.data}, status=status.HTTP_200_OK)


class FoodRecipeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = FoodRecipe.objects.filter(active=True)
    serializer_class = FoodRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        foodRecipes = FoodRecipe.objects.filter(active=True)

        recipe_id = request.query_params.get("recipe_id")
        if recipe_id is not None:
            foodRecipes = foodRecipes.filter(food_recipe_type_id=recipe_id)

        serializer = FoodRecipeSerializer(foodRecipes, many=True)
        return Response(data={"foodRecipes": serializer.data}, status=status.HTTP_200_OK)


class FoodRecipeTypeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = FoodRecipeType.objects.filter(active=True)
    serializer_class = FoodRecipeTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        foodRecipeTypes = FoodRecipeType.objects.filter(active=True)

        serializer = FoodRecipeTypeSerializer(foodRecipeTypes, many=True)
        return Response(data={"foodRecipeTypes": serializer.data}, status=status.HTTP_200_OK)


class MedicineViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Medicine.objects.filter(active=True)
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        medicines = Medicine.objects.filter(active=True)

        serializer = MedicineSerializer(medicines, many=True)
        return Response(data={"medicines": serializer.data}, status=status.HTTP_200_OK)


class MedicineUsageViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = MedicineUsage.objects.filter(active=True)
    serializer_class = MedicineUsageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        usages = MedicineUsage.objects.filter(active=True)

        serializer = MedicineUsageSerializer(usages, many=True)
        return Response(data={"usages": serializer.data}, status=status.HTTP_200_OK)


class MedicineRecipeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = MedicineRecipe.objects.filter(active=True)
    serializer_class = MedicineRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        medicineRecipes = MedicineRecipe.objects.filter(active=True)
        recipe_id = request.query_params.get('recipe_id')
        if recipe_id is not None:
            medicineRecipes = medicineRecipes.filter(
                medicine_recipe_type_id=recipe_id)

        serializer = MedicineRecipeSerializer(medicineRecipes, many=True)
        return Response(data={"medicineRecipes": serializer.data}, status=status.HTTP_200_OK)


class MedicineRecipeTypeViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = MedicineRecipeType.objects.filter(active=True)
    serializer_class = MedicineRecipeTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        medicineRecipes = MedicineRecipeType.objects.filter(active=True)

        serializer = MedicineRecipeTypeSerializer(medicineRecipes, many=True)
        return Response(data={"medicineRecipes": serializer.data}, status=status.HTTP_200_OK)


class DiseaseViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Disease.objects.filter(active=True)
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        diseases = Disease.objects.filter(active=True)

        serializer = DiseaseSerializer(diseases, many=True)
        return Response(data={"diseases": serializer.data}, status=status.HTTP_200_OK)


class WorkViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Work.objects.filter(active=True)
    serializer_class = WorkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        works = Work.objects.filter(active=True)

        serializer = WorkSerializer(works, many=True)
        return Response(data={"works": serializer.data}, status=status.HTTP_200_OK)


class WorkMonitoringViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = WorkMonitoring.objects.filter(active=True)
    serializer_class = WorkMonitoringSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        workMonitorings = WorkMonitoring.objects.filter(active=True)
        performer_id = request.query_params.get('performer_id')
        if performer_id is not None:
            workMonitorings = workMonitorings.filter(performer_id=performer_id)
        care = request.query_params.get('care')
        if care is not None:
            workMonitorings = workMonitorings.filter(care=care)

        serializer = WorkMonitoringSerializer(workMonitorings, many=True)
        return Response(data={"workMonitorings": serializer.data}, status=status.HTTP_200_OK)


class CareScheduleViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = CareSchedule.objects.filter(active=True)
    serializer_class = CareScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        careSchedules = CareSchedule.objects.filter(active=True)

        serializer = CareScheduleSerializer(careSchedules, many=True)
        return Response(data={"careSchedules": serializer.data}, status=status.HTTP_200_OK)


class CareViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Care.objects.filter(active=True)
    serializer_class = CareSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cares = Care.objects.filter(active=True)
        care_schedule_id = request.query_params.get('care_schedule_id')
        if care_schedule_id is not None:
            cares = cares.filter(care_schedule_id=care_schedule_id)

        serializer = CareSerializer(cares, many=True)
        return Response(data={"cares": serializer.data}, status=status.HTTP_200_OK)
