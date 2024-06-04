from models import User, Post, Tag, datetime

from app import db, app


def seed_users():
    users = [
        User(first_name='Ralph', last_name='Stanley'),
        User(first_name='Mitch', last_name='Hedberg', image_URL='https://m.media-amazon.com/images/M/MV5BMTQ0NDAyNDg5OV5BMl5BanBnXkFtZTgwMDUxNjEyMjE@._V1_.jpg'),
        User(first_name='Bill', last_name='Bronsky', image_URL='https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Bronski_Beat_%281985_MCA_publicity_photo%29.jpg/440px-Bronski_Beat_%281985_MCA_publicity_photo%29.jpg'),
        User(first_name='Trey', last_name='Anastasio', image_URL='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXTVvjqGjfQ6cZl1N87YXD02uCtF2JYm7PDMJ8mmSbw-3yMyFp')
    ]
    for user in users:
        db.session.add(user)
        db.session.commit()
    
def seed_posts():
    posts = [
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=1),
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=2),
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=3),
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=4),
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=1),
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=2),
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=3),
        Post(title='The Reason I Play Mandolin', content='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', created_at='2024-01-01 12:00:00', user_id=4)


    ]
    for post in posts:
        db.session.add(post)
        db.session.commit()

def seed_tags():
    tags = [
    Tag(name='First Post'),
    Tag(name='New User'),
    Tag(name='Fun'),
    Tag(name='Excited'),
    Tag(name='Ask Me Anything (AMA)'),
    Tag(name='Birthday Post'),
    Tag(name='Cake Day Post'),
    Tag(name='Help'),
    Tag(name='Advice')

    ]
    for tag in tags:
        db.session.add(tag)
        db.session.commit()
    

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_users()
    seed_posts()
    seed_tags()


