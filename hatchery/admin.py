from django.contrib import admin
from .models import Building,  Care, CareSchedule, Food, FoodRecipe, FoodRecipeType, Medicine, MedicineRecipe, MedicineRecipeType, ReportMonitor, Season, ShrimpStage, ShrimpType, Tank, TankType, User, UserWecon, Work, WorkMonitoring
from .models import Area

admin.site.register(User)
admin.site.register(UserWecon)
admin.site.register(Building)
admin.site.register(Tank)
admin.site.register(TankType)
admin.site.register(Season)
admin.site.register(ShrimpStage)
admin.site.register(ShrimpType)
admin.site.register(Food)
admin.site.register(FoodRecipe)
admin.site.register(FoodRecipeType)
admin.site.register(Medicine)
admin.site.register(MedicineRecipe)
admin.site.register(MedicineRecipeType)
admin.site.register(Work)
admin.site.register(WorkMonitoring)
admin.site.register(CareSchedule)
admin.site.register(Care)
admin.site.register(ReportMonitor)
admin.site.register(Area)
