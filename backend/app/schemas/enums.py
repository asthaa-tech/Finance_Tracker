from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class AccountType(str, Enum):
    BANK = "bank"
    UPI = "upi"
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    OTHER = "other"


class ConnectionStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"


class FamilyRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class MembershipStatus(str, Enum):
    ACTIVE = "active"
    INVITED = "invited"
    REMOVED = "removed"


class CategorizationSource(str, Enum):
    MANUAL = "manual"
    RULE = "rule"
    AI = "ai"
    IMPORTED = "imported"