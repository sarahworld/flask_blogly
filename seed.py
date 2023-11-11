from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Alan", last_name="Alda", image_url="https://www.pngkit.com/png/detail/115-1150342_user-avatar-icon-iconos-de-mujeres-a-color.png")
u2 = User(first_name="John", last_name="Burton",image_url="https://static.vecteezy.com/system/resources/previews/019/896/008/original/male-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png")
u3 = User(first_name="Jane", last_name="Smith", image_url="https://cdn-icons-png.flaticon.com/512/4128/4128253.png")

db.session.add_all([u1,u2,u3]);
db.session.commit();

p1 = Post(title="First Post!", content="Oh, hai.",user_id=1);
p2 = Post(title="First One!", content="Oh, one.",user_id=2);
p3 = Post(title="First!", content="Oh, first.",user_id=3);

db.session.add_all([p1,p2,p3]);
db.session.commit();
