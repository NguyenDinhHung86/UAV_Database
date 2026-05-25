import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UAV:
    name: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    category: Optional[str] = None
    year: Optional[int] = None

    # Technical specs
    weight_g: Optional[float] = None
    max_speed_kmh: Optional[float] = None
    max_altitude_m: Optional[int] = None
    flight_time_min: Optional[int] = None
    range_km: Optional[float] = None
    battery_mah: Optional[int] = None

    # RF parameters
    freq_center_mhz: Optional[float] = None
    freq_bandwidth_mhz: Optional[float] = None
    snr_db: Optional[float] = None
    modulation: Optional[str] = None
    protocol: Optional[str] = None
    freq_hopping: bool = False

    notes: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @staticmethod
    def from_dict(d: dict) -> 'UAV':
        return UAV(**{k: v for k, v in d.items() if k in UAV.__dataclass_fields__})
