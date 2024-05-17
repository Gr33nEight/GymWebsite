from django.contrib import admin
from .models import Workout, Body_Part, Exercise, Workout_Exercise
from import_export.admin import ImportExportModelAdmin

admin.site.register(Workout, ImportExportModelAdmin)
admin.site.register(Body_Part, ImportExportModelAdmin)
admin.site.register(Exercise, ImportExportModelAdmin)
admin.site.register(Workout_Exercise, ImportExportModelAdmin)

