from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timesince import timesince

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)  # เข้าสู่ระบบสำเร็จ
                return redirect('home')  # เปลี่ยนเส้นทางไปยังหน้าหลักหรือหน้าที่ต้องการ
            else:
                form.add_error(None, 'Invalid login credentials')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == "POST":
        form = MemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = MemberRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home_view(request):
    events = Event.objects.all()
    form = EventForm()
    current_user = request.user
    member_data = Member.objects.get(username=current_user.username)
    
    # events = Event.objects.all()
    events = Event.objects.select_related('created_by').all()

    context = {
        'member_data': member_data,
        'form': form,
        'events': events  
    }

    return render(request, 'member/home.html', context)

@login_required
# def profile_view(request):
#     member_data = Member.objects.get(username=request.user.username)
#     return render(request, 'member/profile.html', {'member_data': member_data})
def profile_view(request):
    member_data = Member.objects.get(username=request.user.username)  # ดึงข้อมูลของผู้ใช้ที่ล็อกอิน
    
    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, request.FILES, instance=member_data)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลที่อัปเดต
            return redirect('profile')  # ถ้าฟอร์มถูกต้อง ให้รีไดเรกต์ไปที่หน้าโปรไฟล์
    else:
        form = MemberUpdateForm(instance=member_data)  # กรณีไม่ใช่ POST ให้สร้างฟอร์มจากข้อมูลผู้ใช้ที่ล็อกอิน
    
    return render(request, 'member/profile.html', {'form': form,'member_data': member_data})

def chat_view(request):
    member_data = Member.objects.get(username=request.user.username)
    return render(request, 'member/chat.html', {'member_data': member_data})

@login_required
def new_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  
            event.save()  

            return JsonResponse({'success': True})  
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  

    else:
        form = EventForm() 
    return render(request, 'member/home.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    for event in events:
        event.time_since_created = timesince(event.created_at)  # ใช้ timesince เพื่อคำนวณเวลา
    return render(request, 'your_template.html', {'events': events})

def update_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)  # เชื่อมโยงฟอร์มกับอีเวนต์ที่มีอยู่
        if form.is_valid():
            form.save()  # บันทึกการเปลี่ยนแปลง
            return redirect('home')  # เปลี่ยนเส้นทางไปยังหน้า home หลังจากบันทึกสำเร็จ
    else:
        form = EventForm(instance=event)  # ดึงข้อมูลจากโมเดลเพื่อแสดงในฟอร์ม

    return render(request, 'member/update_event.html', {'form': form})


# ฟังก์ชันสำหรับลบ Event
def delete_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()  
        return redirect('home')  

def search_events(request):
    # กำหนดตัวแปร query สำหรับเก็บคำค้นหาจากฟอร์ม
    member_data = Member.objects.get(username=request.user.username) 
    query = request.GET.get('query', '')
    
    # ใช้ Q objects สำหรับการค้นหาหลายฟิลด์ (event_name, event_title, location)
    events = Event.objects.filter(
        Q(event_name__icontains=query) |
        Q(event_title__icontains=query) |
        Q(location__icontains=query)
    )

    return render(request, 'member/home.html', {'events': events, 'query': query,'member_data': member_data})

# def filter_events(request):
#     member_data = Member.objects.get(username=request.user.username) 
#     category = request.GET.get('category', None)
#     max_participants = request.GET.get('max_participants', None)
#     province = request.GET.get('province', None)

#     events = Event.objects.all()  

#     if category:
#         events = events.filter(category=category)
#     if max_participants:
#         events = events.filter(max_participants__gte=max_participants) 
#     if province:
#         events = events.filter(province=province)

#     return render(request, 'member/home.html', {'events': events,'member_data': member_data})

def filter_events(request):
    province_choices = EventForm.base_fields['province'].choices
    category_choices = EventForm.base_fields['category'].choices

    max_participants_range = range(1, 21)  

    events = Event.objects.all()
    
    province = request.GET.get('province', None)
    category = request.GET.get('category', None)
    max_participants = request.GET.get('max_participants', None)

    if province:
        events = events.filter(province=province)
    if category:
        events = events.filter(category=category)
    if max_participants:
        events = events.filter(max_participants__gte=max_participants)

    return render(request, 'member/home.html', {
        'events': events,
        'province_choices': province_choices,
        'category_choices': category_choices,
        'max_participants_range': max_participants_range,
    })


@login_required
def request_to_join(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    owner = event.owner
    sender = request.user

    # สร้าง Notification
    message = f"{sender.username} ต้องการเข้าร่วมกิจกรรม {event.name} ของคุณ"
    Notification.objects.create(sender=sender, receiver=owner, event=event, message=message)

    return JsonResponse({"message": "Request sent successfully"})


@login_required
def respond_to_request(request, notification_id, action):
    notification = get_object_or_404(Notification, id=notification_id)

    if action == "approve":
        notification.is_approved = True
        notification.save()

        # สร้าง ChatRoom หากยังไม่มี
        chatroom, created = ChatRoom.objects.get_or_create(event=notification.event)
        chatroom.users.add(notification.receiver, notification.sender)

        # แจ้งผู้ขอว่าได้รับการอนุมัติ
        approval_message = f"{notification.receiver.username} ได้ตอบรับคำขอเข้าร่วมกิจกรรม {notification.event.name} ของคุณ"
        Message.objects.create(chatroom=chatroom, sender=notification.receiver, content=approval_message)

        return JsonResponse({"message": "Request approved and chat room created"})

    elif action == "reject":
        notification.is_approved = False
        notification.save()

        # แจ้งผู้ขอว่าถูกปฏิเสธ
        rejection_message = f"{notification.receiver.username} ได้ปฏิเสธคำขอเข้าร่วมกิจกรรม {notification.event.name} ของคุณ"
        Message.objects.create(chatroom=None, sender=notification.receiver, content=rejection_message)

        return JsonResponse({"message": "Request rejected"})

    return JsonResponse({"error": "Invalid action"})


@login_required
def chatroom_view(request, event_id):
    chatroom = get_object_or_404(ChatRoom, event__id=event_id)

    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(chatroom=chatroom, sender=request.user, content=content)

    messages = chatroom.messages.all()
    return render(request, "chatroom.html", {"chatroom": chatroom, "messages": messages})




def logout_view(request):
    logout(request) 
    return redirect('login')  

