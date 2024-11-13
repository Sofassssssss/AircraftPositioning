from typing import Optional
from pydantic import BaseModel, field_validator
from geopy import Point
from config import ureg
from .aircraft import Aircraft


class Flight(BaseModel):
    # Начальная точка полета (может быть объектом Point или кортежем с координатами)
    start_point: Point | tuple[float, float]

    # Конечная точка полета (может быть объектом Point или кортежем с координатами)
    end_point: Point | tuple[float, float]

    # Скорость набора высоты (в футах в минуту). Значение по умолчанию: 2000 футов в минуту.
    climb_rate: ureg.Quantity | int = ureg.Quantity(2000, 'foot/minute')

    # Скорость снижения высоты (в футах в минуту). Значение по умолчанию: 1500 футов в минуту.
    descent_rate: ureg.Quantity | int = ureg.Quantity(1500, 'foot/minute')

    # Крейсерская высота (в футах). Значение по умолчанию: 36000 футов.
    cruise_altitude: ureg.Quantity | int = ureg.Quantity(36000, 'foot')

    # Крейсерская скорость (в километрах в час). Значение по умолчанию: 840 км/ч.
    cruise_speed: ureg.Quantity | int = ureg.Quantity(840, 'km/h')

    # Экземпляр класса Aircraft, представляющий самолет, выполняющий полет.
    aircraft: Aircraft

    # Скорость для начальной фазы набора высоты. Если не указано, используется скорость взлета самолета.
    initial_climb_speed: Optional[ureg.Quantity | int] = None

    # Скорость посадки. Если не указано, используется посадочная скорость самолета.
    landing_speed: Optional[ureg.Quantity | int] = None

    def __init__(self, /, **data):
        super().__init__(**data)
        if self.initial_climb_speed is None:
            self.initial_climb_speed = self.aircraft.takeoff_speed
        if self.landing_speed is None:
            self.landing_speed = self.aircraft.landing_speed

    @field_validator('start_point', 'end_point')
    def convert_to_point(cls, value: any):  # noqa
        if isinstance(value, tuple):
            return Point(value[0], value[1])
        return value

    @field_validator('cruise_altitude')
    def convert_to_foot(cls, value: any):  # noqa
        if isinstance(value, ureg.Quantity):
            return value.to(ureg.foot)
        return value * ureg.foot

    @field_validator('climb_rate', 'descent_rate')
    def convert_to_foot_minute(cls, value: any):  # noqa
        if isinstance(value, ureg.Quantity):
            return value.to(ureg.foot / ureg.minute)
        return value * (ureg.foot / ureg.minute)

    @field_validator('cruise_speed')
    def convert_to_km_h(cls, value: any):  # noqa
        if isinstance(value, ureg.Quantity):
            return value.to(ureg.kilometer / ureg.hour)
        return value * (ureg.kilometer / ureg.hour)

    class Config:
        arbitrary_types_allowed = True
