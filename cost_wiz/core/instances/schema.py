from pydantic import BaseModel


class Ec2InstanceResponseSchema(BaseModel):
    instance_id: str
    instance_type: str
    vcpu: str
    instance_memory: str
    network_performance: str
    on_demand_price: str
    status: str

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


class InstanceRequestSchema(BaseModel):

    instance_id: str
    instance_type: str
    vcpu: str
    instance_memory: str
    network_performance: str
    on_demand_price: str
    status: str
