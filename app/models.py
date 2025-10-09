from django.db import models
from django.contrib.auth.models import User
# Create your models here.



# USER 

class UserProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, null=True,blank=True)
   


# CATEGORIES

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


# EXPENSES

class Expense(models.Model):
    
    user= models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=1000,blank=True, null=True)
    date = models.DateField(auto_now_add=True)


#GROUP

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)


# SPLIT EXPENSE

class SplitExpense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    owner_shared = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_splits")
    friend_shared = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_splits")
    access_type = models.CharField(max_length=20, default="View-Only")





# REPORTS

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    generated_on = models.DateField(auto_now_add=True) 

