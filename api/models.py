import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from api.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    predictions = relationship("SalaryPrediction", back_populates="user")
    logs = relationship("ModelLog", back_populates="user")

class SalaryPrediction(Base):
    __tablename__ = "salary_predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    job_title = Column(String, index=True, nullable=False)
    experience_level = Column(String, nullable=False)
    company_location = Column(String, nullable=False)
    company_size = Column(String, nullable=False)
    remote_ratio = Column(Integer, nullable=False)
    skills = Column(String)
    
    predicted_average = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")

class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, unique=True, index=True, nullable=False)
    category = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    career_paths_as_current = relationship("CareerPath", foreign_keys="CareerPath.current_role_id", back_populates="current_role")
    career_paths_as_next = relationship("CareerPath", foreign_keys="CareerPath.next_role_id", back_populates="next_role")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String)

class CareerPath(Base):
    __tablename__ = "career_paths"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    current_role_id = Column(String, ForeignKey("job_roles.id"), nullable=False)
    next_role_id = Column(String, ForeignKey("job_roles.id"), nullable=False)
    typical_years = Column(Float)
    salary_bump_pct = Column(Float)

    current_role = relationship("JobRole", foreign_keys=[current_role_id], back_populates="career_paths_as_current")
    next_role = relationship("JobRole", foreign_keys=[next_role_id], back_populates="career_paths_as_next")

class CountrySalaryStat(Base):
    __tablename__ = "country_salary_stats"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    country_code = Column(String, index=True, nullable=False)
    avg_salary = Column(Float, nullable=False)
    cost_of_living_index = Column(Float)
    year = Column(Integer, nullable=False)

class ModelLog(Base):
    __tablename__ = "model_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="logs")
