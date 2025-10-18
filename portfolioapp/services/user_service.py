"""
User service for business logic operations
"""
from typing import List, Optional, Tuple
import db
from domain.user import User
from services.exceptions import AuthenticationError, AuthorizationError, ValidationError, DatabaseError

class UserService:
    """Service class for user-related operations"""
    
    @staticmethod
    def authenticate(username: str, password: str) -> Tuple[bool, Optional[User]]:
        """Authenticate a user"""
        try:
            if not username or not password:
                raise ValidationError("Username and password are required")
            
            user = db.users.get(username)
            if user and user.password == password:
                db.logged_in_user = user
                return True, user
            return False, None
        except Exception as e:
            raise DatabaseError(f"Authentication failed: {e}")
    
    @staticmethod
    def logout() -> None:
        """Log out current user"""
        db.logged_in_user = None
    
    @staticmethod
    def get_current_user() -> Optional[User]:
        """Get currently logged in user"""
        return db.logged_in_user
    
    @staticmethod
    def is_admin(user: User) -> bool:
        """Check if user is admin"""
        return user.username == "admin"
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Get all users in the system"""
        return list(db.users.values())
    
    @staticmethod
    def create_user(first_name: str, last_name: str, username: str, 
                   password: str, balance: float) -> Tuple[bool, str]:
        """Create a new user"""
        try:
            # Input validation
            if not first_name or not first_name.strip():
                return False, "First name is required"
            if not last_name or not last_name.strip():
                return False, "Last name is required"
            if not username or not username.strip():
                return False, "Username is required"
            if not password:
                return False, "Password is required"
            if balance < 0:
                return False, "Balance cannot be negative"
            
            # Check for unique username
            if username in db.users:
                return False, "Username already exists"
            
            user = User(first_name.strip(), last_name.strip(), username.strip(), password, balance)
            if db.add_user(user):
                return True, "User created successfully"
            else:
                return False, "Failed to create user"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error creating user: {e}"
    
    @staticmethod
    def delete_user(username: str) -> Tuple[bool, str]:
        """Delete a user"""
        try:
            if not username or not username.strip():
                return False, "Username is required"
            
            username = username.strip()
            
            if username == "admin":
                return False, "Cannot delete admin user"
            
            current_user = db.logged_in_user
            if current_user and current_user.username == username:
                return False, "Cannot delete your own account"
            
            if username not in db.users:
                return False, "User not found"
            
            if db.delete_user(username):
                return True, "User deleted successfully"
            else:
                return False, "Cannot delete user with existing portfolio investments"
        except Exception as e:
            return False, f"Error deleting user: {e}"