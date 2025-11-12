"""
Admin Panel Database Initialization
Sets up admin tables and creates initial super admin accounts
"""

import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import SUPER_ADMINS, Base, User, UserRole, UserStatus


class AdminDatabase:
    """Admin database manager"""

    def __init__(self, db_path="data/admin.db"):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        """Initialize database tables"""
        # Create all tables
        Base.metadata.create_all(self.engine)
        print("✅ Admin database tables created")

        # Create super admin accounts
        self._create_super_admins()

    def _create_super_admins(self):
        """Create super admin accounts for hardcoded emails"""
        session = self.Session()
        try:
            for email in SUPER_ADMINS:
                # Check if already exists
                existing = session.query(User).filter(User.email == email).first()
                if not existing:
                    user = User(
                        email=email,
                        name=email.split("@")[0].replace(".", " ").title(),
                        role=UserRole.SUPER_ADMIN,
                        status=UserStatus.APPROVED,
                        email_verified=True,
                        verified_at=datetime.utcnow(),
                        approved_by="SYSTEM",
                        approved_at=datetime.utcnow(),
                        notes="Super admin - bypasses all rules and restrictions",
                    )
                    session.add(user)
                    print(f"✓ Created super admin: {email}")

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating super admins: {str(e)}")
        finally:
            session.close()

    def get_session(self):
        """Get a new database session"""
        return self.Session()

    def close(self):
        """Close database connection"""
        self.engine.dispose()


# Global instance
_admin_db = None


def get_admin_db():
    """Get or create admin database instance"""
    global _admin_db
    if _admin_db is None:
        _admin_db = AdminDatabase()
    return _admin_db


def init_admin_database():
    """Initialize admin database"""
    db = get_admin_db()
    db.init_db()
    return db
