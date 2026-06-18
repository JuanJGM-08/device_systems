from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    serial_number: str = Field(..., min_length=5)
    device_type: Literal["laptop", "tablet", "projector", "camera", "router", "monitor"]
    brand: Optional[str] = Field(None, max_length=50)
    is_available: bool = True

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=5)
    device_type: Optional[Literal["laptop", "tablet", "projector", "camera", "router", "monitor"]] = None
    brand: Optional[str] = Field(None, max_length=50)
    is_available: Optional[bool] = None

class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)