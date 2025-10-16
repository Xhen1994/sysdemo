from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(self, user_id, username, email, password_hash, role, province=None, 
                 department=None, created_at=None, is_active=True):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.province = province
        self.department = department
        self.created_at = created_at or datetime.now().isoformat()
        self._is_active = is_active  # 使用内部属性
    
    @property
    def is_active(self):
        """重写UserMixin的is_active属性"""
        return self._is_active
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'province': self.province,
            'department': self.department,
            'created_at': self.created_at,
            'is_active': self._is_active  # 使用内部属性
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            user_id=data['id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            role=data['role'],
            province=data.get('province'),
            department=data.get('department'),
            created_at=data.get('created_at'),
            is_active=data.get('is_active', True)
        )
    
    def get_id(self):
        return str(self.id)

