from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/users/%Y/%m', null=True)
    device_token = models.CharField(max_length=50, null=True)
    user_wecon = models.ForeignKey(
        'UserWecon', null=True, on_delete=models.CASCADE)


class ItemBase (models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=150, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class UserWecon(ItemBase):
    class Meta:
        unique_together = ('username', 'role')
    role = models.SmallIntegerField(default=1,)
    username = models.CharField(max_length=150, null=False)
    password = models.CharField(max_length=150, null=False)

    def __str__(self) -> str:
        return self.name


class BuildingType(ItemBase):

    description = models.CharField(max_length=255, null=False)


class Building(ItemBase):

    class Meta:
        unique_together = ('name', 'building_type')

    description = models.CharField(max_length=255, null=False)
    building_type = models.ForeignKey(
        BuildingType, null=False, on_delete=models.CASCADE)
    id_box = models.SmallIntegerField(null=False)


class UnitType(ItemBase):
    pass


class Unit(ItemBase):
    class Meta:
        unique_together = ('name', 'unit_type')
    unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT)


class Tank(ItemBase):

    class Meta:
        unique_together = ('name', 'building')

    Rectangular, Cylinder = range(2)
    Avaiable, Unavaiable = range(2)
    SHAPES = [
        (Rectangular, 'rectangular'),
        (Cylinder, 'cylinder'),
    ]

    STATUS = [
        (Avaiable, 'avaiable'),
        (Unavaiable, 'unavaiable')
    ]

    group_id = models.IntegerField(null=False)
    group_name = models.CharField(max_length=150, null=True)
    length = models.FloatField(null=False)
    height = models.FloatField(null=False)
    width = models.FloatField(null=False)
    shape = models.PositiveSmallIntegerField(
        choices=SHAPES, default=Rectangular)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=Avaiable)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, null=False)

    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)


class TankType(ItemBase):

    description = models.CharField(max_length=255, null=False)


class Season(ItemBase):

    class Meta:
        unique_together = ('name', 'code')

    Draft, InProcess, Ended = range(3)
    STATUS = [
        (Draft, 'Draft'),
        (InProcess, 'InProcess'),
        (Ended, 'Ended')
    ]

    code = models.CharField(max_length=50, null=False)
    start_time = models.DateTimeField(null=False)
    finish_time = models.DateTimeField(null=False)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=Draft)


class ShrimpType(ItemBase):

    description = models.CharField(null=True, max_length=250)


class ShrimpStage(ItemBase):

    shrimp_type = models.ForeignKey(
        ShrimpType, on_delete=models.CASCADE, null=False)
    from_age = models.IntegerField(null=False)
    to_age = models.IntegerField(null=False)
    age_unit = models.ForeignKey(
        Unit, related_name="shrimpstage_age_unit", on_delete=models.SET_NULL, null=True)
    from_length = models.FloatField(null=False)
    to_length = models.FloatField(null=False)
    length_unit = models.ForeignKey(
        Unit, related_name="shrimpstage_length_unit", on_delete=models.SET_NULL, null=True)
    from_weight = models.FloatField(null=False)
    to_weight = models.FloatField(null=False)
    weight_unit = models.ForeignKey(
        Unit, related_name="shrimpstage_weight_unit", on_delete=models.SET_NULL, null=True)
    color = models.CharField(null=True, max_length=150)


class TankPlanning(ItemBase):

    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    breed_numbers = models.FloatField(null=False)
    breed_number_unit = models.ForeignKey(
        Unit, related_name="tankplan_breed_number_unit", on_delete=models.SET_NULL, null=True)
    water_level = models.FloatField(null=False)
    water_level_unit = models.ForeignKey(
        Unit, related_name="tankplan_water_level_unit", on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    tank = models.ForeignKey(Tank, on_delete=models.SET_NULL, null=True)
    tank_type = models.ForeignKey(
        TankType, on_delete=models.SET_NULL, null=True)
    care_schedule = models.ForeignKey(
        'CareSchedule', on_delete=models.SET_NULL, null=True)


class TankMonitoring(ItemBase):

    time = models.DateField(null=False)
    temperature = models.FloatField(null=True)
    temperature_unit = models.ForeignKey(
        Unit, related_name="tankmor_temp_unit", on_delete=models.SET_NULL, null=True)
    water_level = models.FloatField(null=True)
    water_level_unit = models.ForeignKey(
        Unit, related_name="tankmor_water_level_unit", on_delete=models.SET_NULL, null=True)
    ph = models.FloatField(null=True)
    ph_unit = models.ForeignKey(
        Unit, related_name="ph_unit", on_delete=models.SET_NULL, null=True)
    oxygen_concentration = models.FloatField(null=True)
    oxygen_concentration_unit = models.ForeignKey(
        Unit, related_name="tankmor_oxygen_unit", on_delete=models.SET_NULL, null=True)
    tank_planning = models.ForeignKey(
        TankPlanning, on_delete=models.CASCADE, null=False)


class Food(ItemBase):
    class Meta:
        unique_together = ('name', 'building')

    uses = models.CharField(null=True, max_length=250)
    origin = models.CharField(null=True, max_length=150)
    nsx = models.DateField(null=False)
    hsd = models.DateField(null=False)
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True)


class FoodRecipeType(ItemBase):

    comment = models.CharField(null=True, max_length=250)
    building = models.ManyToManyField(
        Building, related_name="food_recipe_type_building", blank=True)
    shrimp_type = models.ForeignKey(
        ShrimpType, on_delete=models.SET_NULL, null=True)
    shrimp_stage = models.ForeignKey(
        ShrimpStage, on_delete=models.SET_NULL, null=True)


class FoodRecipe(ItemBase):
    class Meta:
        unique_together = ('food', 'food_recipe_type')
    food_weight = models.IntegerField()
    food_recipe_type = models.ForeignKey(
        FoodRecipeType, on_delete=models.CASCADE, null=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=False)
    food_weight_unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True)


class Disease(ItemBase):
    reason = models.CharField(null=True, max_length=150)


class MedicineUsage(ItemBase):
    pass


class Medicine(ItemBase):

    Solution, Powder, Pill = range(3)
    FORMS = [
        (Solution, 'Solution'),
        (Powder, 'Powder'),
        (Pill, 'Pill')
    ]

    medicine_form = models.PositiveSmallIntegerField(
        choices=FORMS, default=Solution)
    origin = models.CharField(null=True, max_length=50)
    manufacturer = models.CharField(null=True, max_length=50)
    expired_date = models.DateField(null=False)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, null=True)
    usage = models.ManyToManyField(
        MedicineUsage, related_name="medicine_usage", blank=True)


class MedicineRecipeType(ItemBase):

    description = models.TextField(null=True)
    building = models.ManyToManyField(
        Building, related_name="medicine_recipe_type_building", blank=True)
    shrimp_type = models.ForeignKey(
        ShrimpType, on_delete=models.SET_NULL, null=True)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)


class MedicineRecipe(ItemBase):
    class Meta:
        unique_together = ('medicine', 'medicine_recipe_type')
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, null=False)
    medicine_dosage = models.FloatField(null=False)
    medicine_dosage_unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True)
    medicine_recipe_type = models.ForeignKey(
        MedicineRecipeType, on_delete=models.CASCADE, null=False)


class Work(ItemBase):

    class Meta:
        unique_together = ('name', 'action')

    Feed, Heal, Clean, WaterExchange, Count, Test = range(6)
    ACTIONS = [
        (Feed, 'Feed'),
        (Heal, 'Heal'),
        (Clean, 'Clean'),
        (WaterExchange, 'WaterExchange'),
        (Count, 'Count'),
        (Test, 'Test')
    ]

    action = models.PositiveSmallIntegerField(choices=ACTIONS, default=Feed)
    description = models.CharField(max_length=255, null=False)
    frequency = models.IntegerField(null=False)
    frequency_unit = models.ForeignKey(
        Unit, on_delete=models.SET_NULL, null=True)


class WorkMonitoring(ItemBase):

    Draft, Doing, Done, Cancel, Skipped = range(5)
    STATUS = [
        (Draft, 'Draft'),
        (Doing, 'Doing'),
        (Done, 'Done'),
        (Cancel, 'Cancel'),
        (Skipped, 'Skipped')
    ]

    start_time = models.DateTimeField(null=False)
    finish_time = models.DateTimeField(null=False)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=Draft)
    path = models.ImageField(upload_to='uploads/work/%Y/%m', null=True)
    tank_planning = models.ForeignKey(
        TankPlanning, on_delete=models.CASCADE, null=False)
    work = models.ForeignKey(Work, null=True, on_delete=models.SET_NULL)
    creator_id = models.ForeignKey(
        User, null=True, related_name="creator", on_delete=models.SET_NULL)
    performer_id = models.ForeignKey(
        User, null=True, related_name="performer", on_delete=models.SET_NULL)
    care = models.ForeignKey('Care', null=True, on_delete=models.SET_NULL)


class CareSchedule(ItemBase):
    class Meta:
        unique_together = ('name', 'shrimp_type')
    shrimp_type = models.ForeignKey(
        ShrimpType, on_delete=models.SET_NULL, null=True)


class Care(ItemBase):
    class Meta:
        unique_together = ('name', 'shrimp_stage')

    description = models.CharField(max_length=255, null=True)
    shrimp_stage = models.ForeignKey(
        ShrimpStage, on_delete=models.SET_NULL, null=True)
    care_schedule = models.ForeignKey(
        CareSchedule, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return "Care: " + self.name
