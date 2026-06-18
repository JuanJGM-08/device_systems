from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class LoanUserInfo(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class LoanDeviceInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)

class LoanBase(BaseModel):
    user_id: int
    device_id: int
    status: Literal["active", "returned", "overdue"] = "active"

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    status: Optional[Literal["active", "returned", "overdue"]] = None
    return_date: Optional[datetime] = None

class LoanResponse(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LoanDetailResponse(BaseModel):
    id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: LoanUserInfo
    device: LoanDeviceInfo

    model_config = ConfigDict(from_attributes=True)