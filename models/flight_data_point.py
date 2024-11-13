from pydantic import BaseModel, field_validator
from config import ureg
from geopy import Point


class FlightDataPoint(BaseModel):
    class FlightDataPoint(BaseModel):
        # Время метки (timestamp) в секундах. Может быть передано как целое число или как объект ureg.Quantity.
        timestamp: ureg.Quantity | int

        # Позиция (широта, долгота) в виде объекта Point или кортежа с двумя числами (широта, долгота).
        position: Point | tuple[float, float]

        # Высота (altitude), измеряемая в футах. Может быть передана как целое число или как объект ureg.Quantity.
        altitude: ureg.Quantity | int

    @field_validator('timestamp')
    def convert_to_second(cls, value: any):  # noqa
        if isinstance(value, ureg.Quantity):
            return value.to(ureg.second)
        return value * ureg.second

    @field_validator('position')
    def convert_to_point(cls, value: any):  # noqa
        if isinstance(value, tuple):
            return Point(value[0], value[1])
        return value

    @field_validator('altitude')
    def convert_to_foot(cls, value: any):  # noqa
        if isinstance(value, ureg.Quantity):
            return value.to(ureg.foot)
        return value * ureg.foot

    def __str__(self):
        return (f'{self.timestamp.magnitude},"{self.position.latitude},{self.position.longitude}",'
                f'{int(self.altitude.magnitude) if isinstance(self.altitude, ureg.Quantity) else self.altitude}')

    class Config:
        arbitrary_types_allowed = True
