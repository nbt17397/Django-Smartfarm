from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    building = models.ForeignKey(
        'Building', on_delete=models.CASCADE, null=True)
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
    

class Area(ItemBase):

    Vietnam, Thailand, Cambodia = range(3)
    NATION = [
        (Vietnam, 'vietnam'),
        (Thailand, 'thailand'),
        (Cambodia, 'cambodia')
    ]

    nation = models.PositiveSmallIntegerField(choices=NATION, default=Vietnam)


class Building(ItemBase):

    class Meta:
        unique_together = ('name', 'id_box')

    area_id = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True)
    address = models.CharField(max_length=1000, null=True)
    id_box = models.SmallIntegerField(null=True)

class BuildingDetail(ItemBase):

    class Meta:
        unique_together = ('name', 'id_box')

    building_id = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True, related_name="detail_ids")
    id_box = models.SmallIntegerField(null=True)
    index =  models.SmallIntegerField(null=True, blank=True, default=0)  
    is_running = models.BooleanField(default=True)


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

    description = models.CharField(max_length=1000, null=False)


class Season(ItemBase):

    class Meta:
        unique_together = ('building', 'code')

    code = models.CharField(max_length=50, null=False)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, null=False)
    start_time = models.DateTimeField(null=False)
    finish_time = models.DateTimeField(null=False)


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

    Draft, InProcess, Ended = range(3)
    STATUS = [
        (Draft, 'Draft'),
        (InProcess, 'InProcess'),
        (Ended, 'Ended')
    ]

    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    breed_numbers = models.FloatField(null=False)
    breed_number_unit = models.ForeignKey(
        Unit, related_name="tankplan_breed_number_unit", on_delete=models.SET_NULL, null=True)
    # water_level = models.FloatField(null=False)
    # water_level_unit = models.ForeignKey(
    # Unit, related_name="tankplan_water_level_unit", on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    tank = models.ForeignKey(Tank, on_delete=models.SET_NULL, null=True)
    tank_type = models.ForeignKey(
        TankType, on_delete=models.SET_NULL, null=True)
    # care_schedule = models.ForeignKey(
    # 'CareSchedule', on_delete=models.SET_NULL, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=Draft)
    shrimp_type = models.CharField(null=True, blank=True, max_length=150)
    density = models.CharField(null=True, blank=True, max_length=150)
    rearing_phase = models.CharField(null=True, blank=True, max_length=150) #giai đoạn nuôi
    days_rearing = models.CharField(null=True, blank=True, max_length=150) #ngày nuôi
    


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

    Feed, Heal, Clean, Monitor, Maintenance, About = range(6)
    ACTIONS = [
        (Feed, 'Feed'),
        (Heal, 'Heal'),
        (Clean, 'Clean'),
        (Monitor, 'Monitor'),
        (Maintenance, 'Maintenance'),
        (About, 'About')
    ]

    action = models.PositiveSmallIntegerField(choices=ACTIONS, default=Feed)
    description = models.CharField(max_length=1000, null=False)
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
    tank_planning = models.ForeignKey(
        TankPlanning, related_name="tankPlannings", on_delete=models.CASCADE, null=False)
    work = models.ForeignKey(Work, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=1000, null=True)
    confirm = models.CharField(max_length=1000, null=True)
    creator_id = models.ForeignKey(
        User, null=True, related_name="creator", on_delete=models.SET_NULL)
    performer_id = models.ForeignKey(
        User, null=True, related_name="performer", on_delete=models.SET_NULL)
    path = models.FileField(upload_to='uploads/path/%Y/%m', null=True)


class CareSchedule(ItemBase):
    class Meta:
        unique_together = ('name', 'shrimp_type')
    shrimp_type = models.ForeignKey(
        ShrimpType, on_delete=models.SET_NULL, null=True)


class Care(ItemBase):
    class Meta:
        unique_together = ('name', 'shrimp_stage')

    description = models.CharField(max_length=1000, null=True)
    shrimp_stage = models.ForeignKey(
        ShrimpStage, on_delete=models.SET_NULL, null=True)
    care_schedule = models.ForeignKey(
        CareSchedule, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return "Care: " + self.name


class ReportMonitor(ItemBase):

    tank_planning = models.ForeignKey(
        TankPlanning, related_name="tankPlanning_report", on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to='uploads/file/%Y/%m', null=False)
    creator_id = models.ForeignKey(
        User, null=True, related_name="creator_report", on_delete=models.SET_NULL)


class ResultPlan(ItemBase):

    tank_planning = models.ForeignKey(
        TankPlanning, on_delete=models.CASCADE, null=False)
    result_breed_numbers = models.FloatField(null=False)  # so luong thu duoc
    shrimp_size = models.FloatField(null=False)
    price = models.FloatField(null=False)
    revenue = models.FloatField(null=False)  # san luong thu
    survival_rate = models.FloatField(null=False)  # ti le song
    food_total = models.FloatField(null=False)  # tong thuc an
    revenue_total = models.FloatField(null=False)  # tong thu
    cost = models.FloatField(null=False)
    profit = models.FloatField(null=False)  # loi nhuan
    percent_profit = models.FloatField(null=False)  # % loi nhuan

    def __str__(self) -> str:
        return "ResultPlan: " + self.tank_planning
