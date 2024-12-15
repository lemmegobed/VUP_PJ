from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.conf import settings 
from django.utils import timezone

# class Member(AbstractUser):
#     profile = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default_profile_image.png')
#     sex = models.CharField(max_length=10)
#     birthdate = models.DateField(default=date.today)

#     def __str__(self):
#         return self.username


class Member(AbstractUser):
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default_profile_image.png')
    sex = models.CharField(max_length=10)
    birthdate = models.DateField(blank=True, null=True) 
    description = models.CharField(max_length=30, blank=True, null=True,default='เพิ่มคำอธิบายของคุณ')

    @property
    def age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None 

    def __str__(self):
        return self.username


PROVINCE_CHOICES = [
    ('choose province', 'เลือกจังหวัด'),
    ('Bangkok', 'Bangkok (กรุงเทพมหานคร)'),
    ('Krabi', 'Krabi (กระบี่)'),
    ('Kanchanaburi', 'Kanchanaburi (กาญจนบุรี)'),
    ('Kalasin', 'Kalasin (กาฬสินธุ์)'),
    ('Kamphaeng Phet', 'Kamphaeng Phet (กำแพงเพชร)'),
    ('Khon Kaen', 'Khon Kaen (ขอนแก่น)'),
    ('Chanthaburi', 'Chanthaburi (จันทบุรี)'),
    ('Chachoengsao', 'Chachoengsao (ฉะเชิงเทรา)'),
    ('Chonburi', 'Chonburi (ชลบุรี)'),
    ('Chainat', 'Chainat (ชัยนาท)'),
    ('Chaiyaphum', 'Chaiyaphum (ชัยภูมิ)'),
    ('Chumphon', 'Chumphon (ชุมพร)'),
    ('Chiang Rai', 'Chiang Rai (เชียงราย)'),
    ('Chiang Mai', 'Chiang Mai (เชียงใหม่)'),
    ('Trang', 'Trang (ตรัง)'),
    ('Trat', 'Trat (ตราด)'),
    ('Tak', 'Tak (ตาก)'),
    ('Nakhon Nayok', 'Nakhon Nayok (นครนายก)'),
    ('Nakhon Pathom', 'Nakhon Pathom (นครปฐม)'),
    ('Nakhon Phanom', 'Nakhon Phanom (นครพนม)'),
    ('Nakhon Ratchasima', 'Nakhon Ratchasima (นครราชสีมา)'),
    ('Nakhon Si Thammarat', 'Nakhon Si Thammarat (นครศรีธรรมราช)'),
    ('Nan', 'Nan (น่าน)'),
    ('Nonthaburi', 'Nonthaburi (นนทบุรี)'),
    ('Narathiwat', 'Narathiwat (นราธิวาส)'),
    ('Phayao', 'Phayao (พะเยา)'),
    ('Prachuap Khiri Khan', 'Prachuap Khiri Khan (ประจวบคีรีขันธ์)'),
    ('Pattani', 'Pattani (ปัตตานี)'),
    ('Phra Nakhon Si Ayutthaya', 'Phra Nakhon Si Ayutthaya (พระนครศรีอยุธยา)'),
    ('Phang Nga', 'Phang Nga (พังงา)'),
    ('Phatthalung', 'Phatthalung (พัทลุง)'),
    ('Phichit', 'Phichit (พิจิตร)'),
    ('Phitsanulok', 'Phitsanulok (พิษณุโลก)'),
    ('Phetchaburi', 'Phetchaburi (เพชรบุรี)'),
    ('Phetchabun', 'Phetchabun (เพชรบูรณ์)'),
    ('Phrae', 'Phrae (แพร่)'),
    ('Phuket', 'Phuket (ภูเก็ต)'),
    ('Maha Sarakham', 'Maha Sarakham (มหาสารคาม)'),
    ('Mukdahan', 'Mukdahan (มุกดาหาร)'),
    ('Mae Hong Son', 'Mae Hong Son (แม่ฮ่องสอน)'),
    ('Yasothon', 'Yasothon (ยโสธร)'),
    ('Yala', 'Yala (ยะลา)'),
    ('Roi Et', 'Roi Et (ร้อยเอ็ด)'),
    ('Ranong', 'Ranong (ระนอง)'),
    ('Rayong', 'Rayong (ระยอง)'),
    ('Ratchaburi', 'Ratchaburi (ราชบุรี)'),
    ('Lopburi', 'Lopburi (ลพบุรี)'),
    ('Lampang', 'Lampang (ลำปาง)'),
    ('Lamphun', 'Lamphun (ลำพูน)'),
    ('Loei', 'Loei (เลย)'),
    ('Sisaket', 'Sisaket (ศรีสะเกษ)'),
    ('Sakon Nakhon', 'Sakon Nakhon (สกลนคร)'),
    ('Songkhla', 'Songkhla (สงขลา)'),
    ('Satun', 'Satun (สตูล)'),
    ('Samut Prakan', 'Samut Prakan (สมุทรปราการ)'),
    ('Samut Songkhram', 'Samut Songkhram (สมุทรสงคราม)'),
    ('Samut Sakhon', 'Samut Sakhon (สมุทรสาคร)'),
    ('Sa Kaeo', 'Sa Kaeo (สระแก้ว)'),
    ('Saraburi', 'Saraburi (สระบุรี)'),
    ('Sing Buri', 'Sing Buri (สิงห์บุรี)'),
    ('Sukhothai', 'Sukhothai (สุโขทัย)'),
    ('Suphan Buri', 'Suphan Buri (สุพรรณบุรี)'),
    ('Surat Thani', 'Surat Thani (สุราษฎร์ธานี)'),
    ('Surin', 'Surin (สุรินทร์)'),
    ('Nong Khai', 'Nong Khai (หนองคาย)'),
    ('Nong Bua Lamphu', 'Nong Bua Lamphu (หนองบัวลำภู)'),
    ('Ang Thong', 'Ang Thong (อ่างทอง)'),
    ('Udon Thani', 'Udon Thani (อุดรธานี)'),
    ('Uttaradit', 'Uttaradit (อุตรดิตถ์)'),
    ('Uthai Thani', 'Uthai Thani (อุทัยธานี)'),
    ('Ubon Ratchathani', 'Ubon Ratchathani (อุบลราชธานี)')
]


class Event(models.Model):
    event_name = models.CharField(max_length=50)
    event_title = models.CharField(max_length=100)
    event_datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    province = models.CharField(max_length=100, choices=PROVINCE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now) 
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="events")
    max_participants = models.PositiveIntegerField(default=0)
    # participants = models.ManyToManyField(Member, related_name='events_joined', blank=True)
    

    def __str__(self):
        return self.event_name
    
    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="sent_notifications")
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="received_notifications")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    is_approved = models.BooleanField(null=True, blank=True)  # None = Pending, True = Approved, False = Rejected
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification from {self.sender} to {self.receiver} about {self.event.name}"
    class Meta:
        ordering = ['-created_at']

class ChatRoom(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    users = models.ManyToManyField(Member)

    def __str__(self):
        return f"ChatRoom for {self.event.name}"


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chatroom.event.name}"
    
# class Notification(models.Model):
#     recipient = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="notifications")
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     message = models.CharField(max_length=255)  
#     read = models.BooleanField(default=False)  
#     created_at = models.DateTimeField(auto_now_add=True)  
#     link = models.URLField(max_length=255, null=True, blank=True) 
#     event_id = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
#     request_status = models.CharField(max_length=50, default='Pending')  

#     def __str__(self):
#         return f"Notification for {self.recipient} - {self.message}"

#     class Meta:
#         ordering = ['-created_at']

