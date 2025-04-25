from mongoengine import Document, StringField, DateTimeField,ReferenceField
from datetime import datetime
from Models.user_model import User

class Attendance(Document):
    employee = ReferenceField(User,reverse_delete_rule=2,required=True)
    status = StringField(choices=['absent','present','leave'],required=True)
    data = DateTimeField(default=datetime.now)
    
    def to_json(self):
        return {
            "id": str(self.id),
            'employee':self.employee.to_json() if self.employee else None,
            "status": self.status,
            "data": self.data.strftime("%d %B %Y"),
        }
