from typing import List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.core.exceptions import ConflictException, NotFoundException
from app.models.user import StudentProfile, User
from app.schemas.user import StudentProfileCreate, StudentProfileUpdate, UserCreate


class UserService:
    # -------------------- Users --------------------
    def list_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = (
            select(User)
            .options(selectinload(User.profile))
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def get_user(self, db: Session, user_id: int) -> User:
        stmt = (
            select(User)
            .options(selectinload(User.profile))
            .where(User.id == user_id)
        )
        user = db.scalar(stmt)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found.")
        return user

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.scalar(select(User).where(User.email == email))

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        existing = self.get_user_by_email(db, user_in.email)
        if existing:
            raise ConflictException(f"User with email '{user_in.email}' already exists.")

        user = User(email=user_in.email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # -------------------- Student Profile --------------------
    def get_profile(self, db: Session, user_id: int) -> StudentProfile:
        self.get_user(db, user_id)  # verify user exists
        profile = db.scalar(select(StudentProfile).where(StudentProfile.user_id == user_id))
        if not profile:
            raise NotFoundException(f"Student profile for user id {user_id} not found.")
        return profile

    def upsert_profile(
        self,
        db: Session,
        user_id: int,
        profile_in: StudentProfileCreate,
    ) -> Tuple[StudentProfile, bool]:
        self.get_user(db, user_id)  # verify user exists
        profile = db.scalar(select(StudentProfile).where(StudentProfile.user_id == user_id))

        if profile:
            profile.education = profile_in.education
            profile.year = profile_in.year
            profile.interests = profile_in.interests
            created = False
        else:
            profile = StudentProfile(
                user_id=user_id,
                education=profile_in.education,
                year=profile_in.year,
                interests=profile_in.interests,
            )
            db.add(profile)
            created = True

        db.commit()
        db.refresh(profile)
        return profile, created

    def update_profile(
        self,
        db: Session,
        user_id: int,
        profile_in: StudentProfileUpdate,
    ) -> StudentProfile:
        profile = self.get_profile(db, user_id)

        update_data = profile_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)

        db.commit()
        db.refresh(profile)
        return profile


user_service = UserService()
