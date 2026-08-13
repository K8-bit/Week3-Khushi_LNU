from getpass import getpass

from product import models  # Registers all SQLAlchemy models
from product.db.base import Base
from product.db.session import SessionLocal, engine
from product.models.user import User
from product.repositories.user_repository import get_user_by_email
from product.utils.security import hash_password


def create_first_admin() -> None:
    # Create database tables if they do not already exist.
    Base.metadata.create_all(bind=engine)

    name = input("Admin name: ").strip()
    email = input("Admin email: ").strip().lower()
    mobile = input("Admin mobile: ").strip()
    password = getpass("Admin password: ")

    if not name or not email or not mobile or not password:
        raise SystemExit("All fields are required.")

    db = SessionLocal()

    try:
        existing_user = get_user_by_email(db, email)

        if existing_user is not None:
            raise SystemExit(
                "A user with this email already exists. "
                "No changes were made."
            )

        admin_user = User(
            Name=name,  #Aisha 
            Email=email,  #admin@aisha.com
            Password=hash_password(password),  #aishaadmin
            Mobile=mobile,
            Role="admin",
            IsActive=True,
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"Admin user created successfully: {admin_user.Email}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_first_admin()
