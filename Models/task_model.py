from mongoengine import Document, StringField, DateTimeField,ReferenceField
from datetime import datetime
from Models.user_model import User

class Task(Document):
    manager = ReferenceField("User",reverse_delete_rule=2,required=True)
    employee = ReferenceField("User",reverse_delete_rule=2,required=True)
    task = StringField(required=True)
    status = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    def to_json(self):
        return {
            "id": str(self.id),
            'manager':str(self.manager.id),
            'employee':str(self.employee.id),
            "task": self.task,
            "status": self.status,
            "created_at": self.created_at.strftime("%d %B %Y"),
            "updated_at": self.updated_at.strftime("%d %B %Y"),
        }
