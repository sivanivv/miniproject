from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Category
from django.contrib import messages
from .models import Expense,Report,SplitExpense,Group

# Create your views here.

def index(request):
    return render(request,'index.html')



def adminhomecall(request):
    return render(request,'admin_home.html')

def userhomecall(request):
    user = request.user
    return render(request, 'user_home.html', {'data': [user]})

# def expensecall(request):
#     user = request.user
#     return render(request, 'user_home.html', {'data': [user]})



def Register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        try:
            # Check if username already exists
            if User.objects.filter(username=uname).exists():
                messages.error(request, "⚠ Username already taken. Please choose another.")
                return render(request,'register.html')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "⚠ Email is already registered.")
                return render(request,'register.html')

            # Create the user
            user = User.objects.create_user(
                first_name=fname,
                last_name=lname,
                email=email,
                username=uname,
                password=pword
            )

            # Create associated profile
            UserProfile.objects.create(user_id=user, user_type='regular')

            messages.success(request, "✅ Account created successfully! Please login.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"❌ Something went wrong: {str(e)}")
            return render(request,'register.html')

    return render(request,'register.html')




def Login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        # Check for empty fields
        if not uname or not pword:
            messages.error(request, "⚠ Please enter both username and password.")
            return render(request, 'login.html')

        user = authenticate(request, username=uname, password=pword)
        if user is not None:
            login(request, user)
            try:
                profile = UserProfile.objects.get(user_id=user)
                messages.success(request, f"✅ Loged out!")

                if profile.user_type == 'regular':
                    return redirect('userhome')
                elif profile.user_type == 'admin':
                    return redirect('adminhome')
                else:
                    messages.error(request, "⚠ Unknown user type!")
                    return render(request, 'login.html')

            except UserProfile.DoesNotExist:
                messages.error(request, "❌ No profile found for this user.")
                return render(request, 'login.html')
        else:
            messages.error(request, "❌ Invalid username or password. Try again.")
            return render(request, 'login.html')

    return render(request, 'login.html')



#------------------------------------ADMIN-------------------------------------------------------
#-----------------------------category_management-------------------------------------------------------

def Add_category(request):
    if request.method == 'POST':
        cname = request.POST['category_name']
        if not Category.objects.filter(category_name=cname).exists():
            Category.objects.create(category_name=cname)

    categories = Category.objects.all()
    return render(request, 'category_management.html', {'categories': categories})

def Catdelete(request,id):
    j=Category.objects.get(id=id)
    j.delete()
    return redirect('category')

def Catedit(request,id):
    cat=Category.objects.get(id=id)
    if request.method=='POST':
        cat.category_name=request.POST['category_name']
       
        cat.save()
        return redirect('category')

    else:
        return render(request,'category_edit.html',{'da':cat})
    
#-----------------------------users_management--------------------------------------------------------



def User_management(request):
    all=UserProfile.objects.filter(user_type='regular')
    return render(request,'users_management.html',{'users':all})

def Userdelete(request,id):
    ed=User.objects.get(id=id)
    ed.delete()
    return redirect('users')


#--------------------------------admin_report----------------------------------------------------------


    


#------------------------------------USERS--------------------------------------------------------------
#-----------------------------expense_management--------------------------------------------------------


def Add_expense(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        category_id = int(request.POST['category'])
        amount = request.POST['amount']
        description = request.POST.get('description', '')
        date=request.POST['date']
        user = request.user
        category = Category.objects.get(id=category_id)

        Expense.objects.create(user=user, category=category, amount=amount, description=description,date=date)
        return redirect('expense')  

    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-id')
    total_amount = sum(exp.amount for exp in expenses)

    return render(request, 'expense.html', {'categories': categories,'expenses': expenses,'total_amount': total_amount})


def Exdelete(request,id):
    ed=Expense.objects.get(id=id)
    ed.delete()
    return redirect('expense')

def Exedit(request, id):
    exed = Expense.objects.get(id=id)
    categories = Category.objects.all()  

    if request.method == 'POST':
        category_id = int(request.POST['category'])
        category = Category.objects.get(id=category_id)

        exed.category = category
        exed.amount = request.POST['amount']
        exed.description = request.POST.get('description', '')

        exed.save()
        return redirect('expense')

    return render(request, 'expense_edit.html', {'da': exed,'categories': categories })



#-----------------------------categorized_tracking--------------------------------------------------------


def Categorized_tracking(request):
    user_id = request.user.id  
    categories = Category.objects.all()
    data = []
    for category in categories:
        expenses = Expense.objects.filter(user_id=user_id, category_id=category.id)
        if expenses.exists():
            total_amount = sum(e.amount for e in expenses)
            data.append({'category_name': category.category_name,'expenses': expenses,'total': total_amount })
    return render(request, 'categorized_tracking.html', {'data': data})



#-----------------------------report_generation--------------------------------------------------------


def report_page(request):
    expenses = []
    total_amount = 0
    rtype = ""

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        rtype = request.POST['report_type']
        expenses = Expense.objects.filter(
            user=request.user, 
            date__gte=start_date, 
            date__lte=end_date
        )
        total_amount = sum(exp.amount for exp in expenses)

        Report.objects.create(
            user=request.user,
            report_type=rtype,
            start_date=start_date,
            end_date=end_date,
            total_amount=total_amount
        )

    return render(request, 'report_generation.html', {
        'expenses': expenses,
        'total_amount': total_amount,
        'rtype': rtype
    })



#-----------------------------split_expense--------------------------------------------------------


def Groups(request):
    friends = User.objects.exclude(id=request.user.id)
    groups = Group.objects.filter(members=request.user)

    if request.method == 'POST':
        name = request.POST['name']
        member_ids = request.POST.getlist('members')
        group = Group.objects.create(name=name)
        group.members.add(request.user)
        for fid in member_ids:
            user = User.objects.get(id=fid)
            group.members.add(user)
        return redirect('groups')

    return render(request, 'group.html', {'friends': friends, 'groups': groups})


from .models import Notification

def Group_detail(request, id):
    group = Group.objects.get(id=id)
    members = group.members.all()

    if request.method == 'POST':
        desc = request.POST['description']
        amount = float(request.POST['amount'])
        owner = request.user

        # Create the main expense
        exp = Expense.objects.create(user=owner, category=None, amount=amount, description=desc)
        per_person = amount / members.count()

        # Create split records for each member
        for m in members:
            SplitExpense.objects.create(
                group=group,
                expense=exp,
                owner_shared=owner,
                friend_shared=m,
                access_type="View-Only"
            )

            # ✅ Send notification to other members (not the one who added)
            if m != owner:
                Notification.objects.create(
                    user=m,
                    message=f"{owner.username} added a new expense '{desc}' in group '{group.name}'. Your share is ₹{per_person:.2f}."
                )

        return redirect('group_detail', id=id)

    # Get all split expenses for this group
    split_expenses = SplitExpense.objects.filter(group=group).order_by('-id')

    # Prepare structured data for display
    grouped_data = {}
    for se in split_expenses:
        exp_id = se.expense.id
        if exp_id not in grouped_data:
            grouped_data[exp_id] = {
                'description': se.expense.description,
                'amount': se.expense.amount,
                'owner': se.owner_shared.username,
                'members': [],
                'split_amount': float(se.expense.amount) / group.members.count(),
            }
        grouped_data[exp_id]['members'].append(se.friend_shared.username)

    return render(request, 'group_details.html', {
        'group': group,
        'grouped_data': grouped_data.values(),
    })


def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': user_notifications})



from django.contrib.auth.models import auth
def Logout(request):
    auth.logout(request)
    return redirect('login')