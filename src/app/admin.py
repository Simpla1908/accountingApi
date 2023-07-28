from django.contrib import admin
from .models import CustomUser,entreprises,classes,categories,comptes,souscomptes,journaux,exercices

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(entreprises)
admin.site.register(classes)
admin.site.register(categories)
admin.site.register(comptes)
admin.site.register(souscomptes)
admin.site.register(journaux)
admin.site.register(exercices)



