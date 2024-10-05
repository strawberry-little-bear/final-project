# events/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import VolunteerEvent, VolunteerParticipation
from django.contrib.auth.decorators import login_required

def event_list(request):
    events = VolunteerEvent.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
        event = VolunteerEvent.objects.create(
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            organizer=request.user
        )
        return redirect('event_detail', event_id=event.id)

    return render(request, 'events/create_event.html')

from django.shortcuts import render, get_object_or_404
from .models import VolunteerEvent, VolunteerParticipation
from django.contrib.auth.decorators import login_required

def event_detail(request, event_id):
    event = get_object_or_404(VolunteerEvent, id=event_id)
    
    # 检查用户是否已经参与该活动
    user_has_joined = False
    if request.user.is_authenticated:
        user_has_joined = VolunteerParticipation.objects.filter(event=event, user=request.user).exists()

    print(f"User: {request.user}, Event: {event.title}, User has joined: {user_has_joined}")

    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_has_joined': user_has_joined,  # 传递用户是否参与的信息
    })


from django.contrib import messages

@login_required
def join_event(request, event_id):
    event = get_object_or_404(VolunteerEvent, id=event_id)
    if not VolunteerParticipation.objects.filter(event=event, user=request.user).exists():
        VolunteerParticipation.objects.create(event=event, user=request.user)
        messages.success(request, f'成功参与活动: {event.title}')  # 添加成功消息
    else:
        messages.info(request, '您已参与该活动。')  # 添加已参与消息
    
    return redirect('event_detail', event_id=event.id)




# events/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # 保存用户
            username = form.cleaned_data.get('username')
            messages.success(request, f'账号 {username} 创建成功！现在可以登录了。')
            return redirect('login')  # 成功后跳转到登录页面
    else:
        form = UserRegisterForm()
    return render(request, 'events/register.html', {'form': form})

# events/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VolunteerEvent
from django.utils import timezone

@login_required  # 确保只有登录的用户可以发布活动
def create_event(request):
    if request.method == 'POST':
        # 获取表单数据
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # 创建并保存活动
        event = VolunteerEvent.objects.create(
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            organizer=request.user
        )

        return redirect('event_detail', event_id=event.id)  # 成功后重定向到活动详情页

    return render(request, 'events/create_event.html')

from django.contrib import messages

@login_required
def cancel_participation(request, event_id):
    event = get_object_or_404(VolunteerEvent, id=event_id)
    participation = VolunteerParticipation.objects.filter(event=event, user=request.user)
    
    if participation.exists():
        participation.delete()
        messages.success(request, f'你已取消参与活动: {event.title}')
    else:
        messages.error(request, '你未参与该活动，无法取消。')
    
    return redirect('event_detail', event_id=event.id)

from django.shortcuts import render
from .models import VolunteerParticipation

@login_required
def profile(request):
    participations = VolunteerParticipation.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/profile.html', {
        'participations': participations
    })
