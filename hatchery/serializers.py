from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Building, BuildingType, Care, CareSchedule, Disease, Food, FoodRecipe, FoodRecipeType, Medicine, MedicineRecipe, MedicineRecipeType, MedicineUsage, Season, ShrimpStage, ShrimpType, Tank, TankMonitoring, TankPlanning, TankType, Unit, UnitType, User, UserWecon, Work, WorkMonitoring


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email",
                  "username", "password", "date_joined", "avatar", "user_wecon"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserWeconSerializer(ModelSerializer):

    class Meta:
        model = UserWecon
        fields = ["id", "username", "password", "role", "name", "active"]


class BuildingTypeSerializer(ModelSerializer):

    class Meta:
        model = BuildingType
        fields = ["id", "name", "description", "active"]


class BuildingSerializer(ModelSerializer):

    class Meta:
        model = Building
        fields = ["id", "name", "description",
                  "building_type", "active", "id_box"]


class UnitTypeSerializer(ModelSerializer):

    class Meta:
        model = UnitType
        fields = ["id", "name", "active"]


class UnitSerializer(ModelSerializer):

    class Meta:
        model = Unit
        fields = ["id", "name", "active", "unit_type"]


class TankSerializer(ModelSerializer):

    class Meta:
        model = Tank
        fields = ["id", "name", "length", "height",
                  "width", "shape", "status", "building", "unit", "group_name",
                  "group_id"]


class TankTypeSerializer(ModelSerializer):

    class Meta:
        model = TankType
        fields = ["id", "name", "description"]


class SeasonSerializer(ModelSerializer):

    class Meta:
        model = Season
        fields = ["id", "name", "start_time", "finish_time", "status", "code"]


class ShrimpTypeSerializer(ModelSerializer):

    class Meta:
        model = ShrimpType
        fields = ["id", "name", "description"]


class ShrimpStageSerializer(ModelSerializer):

    class Meta:
        model = ShrimpStage
        fields = ["id", "name", "shrimp_type", "from_age", "to_age", "age_unit",
                  "from_length", "to_length", "length_unit", "from_weight", "to_weight", "weight_unit", "color"]


class TankPlanningSerializer(ModelSerializer):

    class Meta:
        model = TankPlanning
        fields = ["id", "name", "manager", "breed_numbers", "breed_number_unit", "water_level",
                  "water_level_unit", "season", "tank", "tank_type", "care_schedule"]


class TankMonitoringSerializer(ModelSerializer):

    class Meta:
        model = TankMonitoring
        fields = ["id", "time", "temperature", "temperature_unit", "water_level", "water_level_unit",
                  "ph", "ph_unit", "oxygen_concentration", "oxygen_concentration_unit", "tank_planning"]


class FoodSerializer(ModelSerializer):

    class Meta:
        model = Food
        fields = ["id", "name", "uses", "nsx", "hsd", "origin", "building"]


class FoodRecipeTypeSerializer(ModelSerializer):

    class Meta:
        model = FoodRecipeType
        fields = ["id", "name", "comment",
                  "building", "shrimp_type", "shrimp_stage"]


class FoodRecipeSerializer(ModelSerializer):

    class Meta:
        model = FoodRecipe
        fields = ["id", "food_weight",
                  "food_recipe_type", "food", "food_weight_unit"]


class MedicineUsageSerializer(ModelSerializer):

    class Meta:
        model = MedicineUsage
        fields = ["id", "name"]


class MedicineSerializer(ModelSerializer):

    class Meta:
        model = Medicine
        fields = ["id", "name", "medicine_form", "origin", "manufacturer",
                  "import_no", "expired_date", "building", "usage"]


class MedicineRecipeTypeSerializer(ModelSerializer):
    class Meta:
        model = MedicineRecipeType
        fields = ["id", "name", "description", "building", "shrimp_type"]


class MedicineRecipeSerializer(ModelSerializer):

    class Meta:
        model = MedicineRecipe
        fields = ["id", "medicine", "medicine_dosage",
                  "medicine_dosage_unit", "medicine_recipe_type", "disease"]


class DiseaseSerializer(ModelSerializer):

    class Meta:
        model = Disease
        fields = ["id", "name", "reason"]


class WorkSerializer(ModelSerializer):

    class Meta:
        model = Work
        fields = ["id", "name", "description", "action", "frequency", "frequency_unit"
                  ]


class WorkMonitoringSerializer(ModelSerializer):

    class Meta:
        model = WorkMonitoring
        fields = ["id", "start_time", "finish_time", "creator_id", "performer_id",
                  "status", "path", "tank_planning", "work", "care"]


class CareSerializer(ModelSerializer):
    shrimp_stage = ShrimpStageSerializer

    class Meta:
        model = Care
        fields = ["id", "name", "shrimp_stage", "care_schedule"]


class CareScheduleSerializer(ModelSerializer):

    class Meta:
        model = CareSchedule
        fields = ["id", "name", "shrimp_type"]
