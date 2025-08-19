from datetime import date
from myapp.models import Person, Group, Membership  # Thay 'myapp' bằng tên app của bạn

# --- Tạo Person ---
ringo = Person.objects.create(first_name="Ringo", last_name="Starr")
paul = Person.objects.create(first_name="Paul", last_name="McCartney")
john = Person.objects.create(first_name="John", last_name="Lennon")
george = Person.objects.create(first_name="George", last_name="Harrison")

# --- Tạo Group ---
beatles = Group.objects.create(name="The Beatles")

# --- Tạo Membership trực tiếp ---
m1 = Membership(person=ringo, group=beatles, date_joined=date(1962, 8, 16), invite_reason="Needed a new drummer.")
m1.save()
m2 = Membership.objects.create(person=paul, group=beatles, date_joined=date(1960, 8, 1), invite_reason="Wanted to form a band.")
print("Members after initial Memberships:", beatles.members.all())

# --- Thêm John và George bằng add() và create() ---
# beatles.members.add(john, through_defaults={"date_joined": date(1960, 8, 1)})
# beatles.members.create(first_name="George", last_name="Harrison", through_defaults={"date_joined": date(1960, 8, 1)})
# print("Members after add and create:", beatles.members.all())

#Sử dụng set() để cập nhật danh sách thành viên
# beatles.members.set([john, paul, ringo, george], through_defaults={"date_joined": date(1960, 8, 1)})
# print("Members after set:", beatles.members.all())

#Tạo nhiều Membership cho Ringo
# Membership.objects.create(
#     person=ringo,
#     group=beatles,
#     date_joined=date(1968, 9, 4),
#     invite_reason="You've been gone for a month and we miss you."
# )
# print("Members after adding Ringo again:", beatles.members.all())

#Xóa tất cả Membership của Ringo
# beatles.members.remove(ringo)
# print("Members after removing Ringo:", beatles.members.all())

#Xóa toàn bộ Membership của Group
# beatles.members.clear()
# print("All Memberships after clearing beatles:", Membership.objects.all()) 
#Query: Tìm tất cả các nhóm có thành viên tên bắt đầu bằng "Paul"
# groups_with_paul = Group.objects.filter(members__first_name__startswith="Paul")
# print("Groups with a member whose name starts with 'Paul':", groups_with_paul)
#Query: Tìm các thành viên của Beatles gia nhập sau 1,1,196
# members_after_1961 = Person.objects.filter(
#     group__name="The Beatles",
#     membership__date_joined__gt=date(1961, 1, 1)
# )
# print("Members of Beatles who joined after 1 Jan 1961:", members_after_1961)
#Truy cập thông tin Membership trực tiếp
# ringos_membership = Membership.objects.get(group=beatles, person=ringo)
# print("Ringo's date joined:", ringos_membership.date_joined)  # 1962-08-16
# print("Ringo's invite reason:", ringos_membership.invite_reason)  # 'Needed a new drummer.'

#Truy cập thông tin Membership thông qua reverse relation từ Person
# ringos_membership_alt = ringo.membership_set.get(group=beatles)
# print("Ringo's date joined (reverse):", ringos_membership_alt.date_joined)
# print("Ringo's invite reason (reverse):", ringos_membership_alt.invite_reason)