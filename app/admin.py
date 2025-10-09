from django.contrib import admin
from .models import UserProfile
from .models import Category
from .models import Expense
from .models import SplitExpense
from .models import Report,Group


# Register your models here.



admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(SplitExpense)
admin.site.register(Report)
admin.site.register(Group)
