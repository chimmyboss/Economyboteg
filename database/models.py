"""
Database Models
SQLAlchemy ORM models for ECON Discord Bot
"""

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Enum, 
    ForeignKey, UniqueConstraint, func, JSON, DECIMAL
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

Base = declarative_base()


class AccountType(str, enum.Enum):
    """Account type enum."""
    PERSONAL_WALLET = "personal-wallet"
    PERSONAL_BANK = "personal-bank"
    BUSINESS = "business"
    DEPARTMENT = "department"


class Guilds(Base):
    """Guild/Server data model."""
    __tablename__ = "guilds"
    
    IDENT = Column(String, primary_key=True)  # Guild ID
    balance = Column(DECIMAL(20, 2), nullable=False, default=0.0)
    logging_channel = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    guild_members = relationship("GuildMembers", back_populates="guild")
    accounts = relationship("Accounts", back_populates="guild_obj")
    departments = relationship("Department", back_populates="guild_obj")
    shifts = relationship("Shift", back_populates="guild_obj")


class DiscordUsers(Base):
    """Discord user data model."""
    __tablename__ = "discord_users"
    
    IDENT = Column(String, primary_key=True)  # User ID
    username = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    guild_members = relationship("GuildMembers", back_populates="user")


class GuildMembers(Base):
    """Guild member data model."""
    __tablename__ = "guild_members"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    user = Column(String, ForeignKey("discord_users.IDENT"), nullable=False)
    nickname = Column(String, nullable=True)
    presence = Column(String, default="ACTIVE")  # ACTIVE or INACTIVE
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('guild', 'user', name='unique_guild_member'),
    )
    
    # Relationships
    guild_obj = relationship("Guilds", back_populates="guild_members")
    user_obj = relationship("DiscordUsers", back_populates="guild_members")
    accounts = relationship("Accounts", back_populates="owner_obj")


class Accounts(Base):
    """Account data model."""
    __tablename__ = "accounts"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    owner = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    balance = Column(DECIMAL(20, 2), nullable=False, default=0.0)
    type = Column(Enum(AccountType), nullable=False)
    description = Column(String, nullable=True)
    name = Column(String, nullable=True)
    message = Column(String, nullable=True)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    guild_obj = relationship("Guilds", back_populates="accounts")
    owner_obj = relationship("GuildMembers", back_populates="accounts")
    transaction_logs = relationship("TransactionLogs", back_populates="account")


class TransactionLogs(Base):
    """Transaction log model."""
    __tablename__ = "transaction_logs"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account = Column(String, ForeignKey("accounts.IDENT"), nullable=False)
    amount = Column(DECIMAL(20, 2), nullable=False)
    transaction_type = Column(String, nullable=False)  # deposit, withdrawal, transfer
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    account_obj = relationship("Accounts", back_populates="transaction_logs")


class Department(Base):
    """Department model."""
    __tablename__ = "departments"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    account_id = Column(String, ForeignKey("accounts.IDENT"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    guild_obj = relationship("Guilds", back_populates="departments")
    members = relationship("DepartmentMembers", back_populates="department_obj")
    roles = relationship("DepartmentRoles", back_populates="department_obj")


class DepartmentMembers(Base):
    """Department member model."""
    __tablename__ = "department_members"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    department = Column(String, ForeignKey("departments.IDENT"), nullable=False)
    member = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    role = Column(String, nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    department_obj = relationship("Department", back_populates="members")


class DepartmentRoles(Base):
    """Department role model."""
    __tablename__ = "department_roles"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    department = Column(String, ForeignKey("departments.IDENT"), nullable=False)
    role_name = Column(String, nullable=False)
    permissions = Column(JSON, nullable=True)  # JSON array of permissions
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    department_obj = relationship("Department", back_populates="roles")


class Inventory(Base):
    """Inventory model."""
    __tablename__ = "inventory"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Items(Base):
    """Items model."""
    __tablename__ = "items"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    inventory = Column(String, ForeignKey("inventory.IDENT"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    value = Column(DECIMAL(20, 2), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Citation(Base):
    """Citation model."""
    __tablename__ = "citations"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    issuer = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    violator = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    reason = Column(String, nullable=False)
    amount = Column(DECIMAL(20, 2), nullable=False)
    status = Column(String, default="PENDING")  # PENDING, PAID, DISMISSED
    issued_at = Column(DateTime, default=datetime.utcnow)


class Shift(Base):
    """Work shift model."""
    __tablename__ = "shifts"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    member = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    pay_rate = Column(DECIMAL(20, 2), nullable=False)
    total_pay = Column(DECIMAL(20, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    guild_obj = relationship("Guilds", back_populates="shifts")


class Fee(Base):
    """Fee/Tax model."""
    __tablename__ = "fees"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    name = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuthorizedUsers(Base):
    """Authorized users model (for command permissions)."""
    __tablename__ = "authorized_users"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    user = Column(String, nullable=False)
    permission_level = Column(Integer, default=1)  # 1=mod, 2=admin, 3=owner
    created_at = Column(DateTime, default=datetime.utcnow)


class AdvTransactionLogs(Base):
    """Advanced transaction logs model."""
    __tablename__ = "adv_transaction_logs"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    from_account = Column(String, ForeignKey("accounts.IDENT"), nullable=True)
    to_account = Column(String, ForeignKey("accounts.IDENT"), nullable=True)
    amount = Column(DECIMAL(20, 2), nullable=False)
    transaction_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class MoneyPrints(Base):
    """Money printing record model."""
    __tablename__ = "money_prints"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    amount = Column(DECIMAL(20, 2), nullable=False)
    created_by = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class RolePay(Base):
    """Role-based pay configuration model."""
    __tablename__ = "role_pay"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    role_id = Column(String, nullable=False)
    pay_amount = Column(DECIMAL(20, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SellRecords(Base):
    """Sell/Trade records model."""
    __tablename__ = "sell_records"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    seller = Column(String, ForeignKey("guild_members.IDENT"), nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(DECIMAL(20, 2), nullable=False)
    total_price = Column(DECIMAL(20, 2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Modals(Base):
    """Modal/Form data model."""
    __tablename__ = "modals"
    
    IDENT = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guild = Column(String, ForeignKey("guilds.IDENT"), nullable=False)
    user = Column(String, nullable=False)
    modal_type = Column(String, nullable=False)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
