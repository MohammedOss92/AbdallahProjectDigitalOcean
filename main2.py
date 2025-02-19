import os
import django

# 1. تهيئة بيئة Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Abdallah_Project.settings')  # ضع اسم مشروعك هنا
django.setup()

from Msgs_Api.models import Messages, MeesageType  # استبدل باسم تطبيقك ونموذج MessageType

# 2. قراءة النصوص من الملف
file_path = r"/root/Abdallah_Project3/a (299).txt"
#file_paths = [
#    r"/root/Abdallah_Project3/a (1).txt",  # الملف الأول
#    r"/root/Abdallah_Project3/a (2).txt",  # الملف الثاني
#    r"/root/Abdallah_Project3/a (3).txt"   # الملف الثالث
#]

with open(file_path, "r", encoding="utf8") as file:
    content = file.read()

# 3. تقسيم النصوص بناءً على الفاصل
rows = [row.strip() for row in content.split("----") if row.strip()]

# 4. إدخال النصوص في قاعدة البيانات
id_type_instance = MeesageType.objects.get(id=1)  # استبدل هذا بمعرف النوع ID_Type

for row in rows:
    Messages.objects.create(
        MessageName=row,
        ID_Type=id_type_instance,
        new_msgs="1",
        new_msgs_text="1",
        day_num="0",
    )

print("تم إدخال النصوص بنجاح إلى قاعدة البيانات!")
print(Messages.objects.count())  