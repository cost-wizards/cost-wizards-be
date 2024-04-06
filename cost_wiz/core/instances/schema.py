from pydantic import BaseModel


class Ec2InstanceResponseSchema(BaseModel):
    instance_id: str
    instance_type: str
    status: str
    cpu: int
    ram: str
    price: float

    class Config:
        from_attributes = True


class InstanceResponseSchema(BaseModel):
    id: int
    name: str
    instance_id: str
    instance_type: str
    cpu: str
    ram: str
    status: str
    hourly_rate: float

    class Config:
        from_attributes = True
