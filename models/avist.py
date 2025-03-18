from sqlmodel import Field, Column, Integer, ForeignKey, SQLModel, DECIMAL
from decimal import Decimal

class Avist(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    long: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10,2)))
    lati: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10,2)))
    
    user_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("users.id")))
    distrito_id : int = Field(default=None, sa_column=Column(Integer, ForeignKey("distrito.id")))