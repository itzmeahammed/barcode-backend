from mongoengine import Document, StringField, IntField, FloatField, DateTimeField,ReferenceField
from datetime import datetime
from Models.user_model import User

class Invoice(Document):
    user= ReferenceField(User,reverse_delete_rule=2,required=True)
    name = StringField(required=True)
    category = StringField(required=True)
    price = FloatField(required=True)
    unit = StringField(required=True)
    stock = IntField(required=True)
    expiry_date = StringField(required=True)
    image = StringField()
    brand = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    def to_json(self):
        return {
            "id": str(self.id),
            'user':str(self.user.id),
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "unit": self.unit,
            "stock": self.stock,
            "image":self.image,
            "expiry_date": self.expiry_date,
            "brand": self.brand,
            "created_at": self.created_at.strftime("%d %B %Y"),
            "updated_at": self.updated_at.strftime("%d %B %Y"),
        }
