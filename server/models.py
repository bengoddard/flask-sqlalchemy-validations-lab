from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, Aname):
        if not Aname:
            raise ValueError("Name must be present.")
        duplicate_name = db.session.query(Author.id).filter_by(name = Aname).first()
        if duplicate_name is not None:
            raise ValueError("Name must be unique.")
        return Aname

    @validates('phone_number')
    def validate_phone(self, key, phone):
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(phone) > 10:
            raise ValueError("Phone number is too long.")
        if len(phone) < 10:
            raise ValueError("Phone number is too short.")
        return phone

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content')
    def validate_text(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary can not be longer than 250 characters.")
        return summary
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ["Fiction", "Non-Fiction"]
        if category not in valid_categories:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'.")
        return category
    @validates('title')
    def validate_title(self, key, title):
        keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in keywords):
            raise ValueError("Title must contain one of the following: "
                "'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
