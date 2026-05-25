import json
import os
from typing import List, Optional
from uav_model import UAV

DB_PATH = os.path.join(os.path.dirname(__file__), "uav_data.json")


class UAVDatabase:
    def __init__(self):
        self._uavs: List[UAV] = []
        self._load()

    # ── Persistence ──────────────────────────────────────
    def _load(self):
        if os.path.exists(DB_PATH):
            with open(DB_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self._uavs = [UAV.from_dict(d) for d in raw]
        else:
            self._uavs = _seed_data()
            self.save()

    def save(self):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in self._uavs], f,
                      ensure_ascii=False, indent=2)

    # ── CRUD ─────────────────────────────────────────────
    def get_all(self) -> List[UAV]:
        return list(self._uavs)

    def get_by_id(self, uid: str) -> Optional[UAV]:
        return next((u for u in self._uavs if u.id == uid), None)

    def add(self, uav: UAV):
        self._uavs.append(uav)
        self.save()

    def delete(self, uid: str):
        self._uavs = [u for u in self._uavs if u.id != uid]
        self.save()

    def search(self, query: str, category: str = None) -> List[UAV]:
        q = query.lower().strip()
        results = []
        for u in self._uavs:
            if category and u.category != category:
                continue
            haystack = f"{u.name} {u.manufacturer or ''} {u.model or ''} {u.protocol or ''} {u.modulation or ''}".lower()
            if q in haystack:
                results.append(u)
        return results


# ── Seed data — 20 UAV thực tế ────────────────────────────────────────
def _seed_data() -> List[UAV]:
    return [
        UAV(name="DJI Phantom 4 Pro V2",
            manufacturer="DJI", model="Phantom 4 Pro V2", category="Professional",
            year=2018, weight_g=1375, max_speed_kmh=72, max_altitude_m=6000,
            flight_time_min=30, range_km=7, battery_mah=5870,
            freq_center_mhz=2400, freq_bandwidth_mhz=80, snr_db=22,
            modulation="OFDM", protocol="OcuSync 2.0", freq_hopping=True,
            notes="Cảm biến ảnh 1 inch, 20 MP. Dòng flagship chuyên nghiệp của DJI."),

        UAV(name="DJI Mavic 3 Pro",
            manufacturer="DJI", model="Mavic 3 Pro", category="Professional",
            year=2023, weight_g=958, max_speed_kmh=75.6, max_altitude_m=6000,
            flight_time_min=43, range_km=15, battery_mah=5000,
            freq_center_mhz=2400, freq_bandwidth_mhz=100, snr_db=25,
            modulation="OFDM", protocol="O3", freq_hopping=True,
            notes="3 camera tele, cảm biến 4/3 inch Hasselblad. Flagship 2023."),

        UAV(name="DJI Mini 4 Pro",
            manufacturer="DJI", model="Mini 4 Pro", category="Consumer",
            year=2023, weight_g=249, max_speed_kmh=57.6, max_altitude_m=4000,
            flight_time_min=34, range_km=20, battery_mah=2590,
            freq_center_mhz=2400, freq_bandwidth_mhz=60, snr_db=20,
            modulation="OFDM", protocol="O4", freq_hopping=True,
            notes="Dưới 250g, không cần đăng ký ở nhiều quốc gia."),

        UAV(name="DJI FPV Combo",
            manufacturer="DJI", model="FPV", category="Racing",
            year=2021, weight_g=795, max_speed_kmh=140, max_altitude_m=6000,
            flight_time_min=20, range_km=10, battery_mah=2000,
            freq_center_mhz=5800, freq_bandwidth_mhz=150, snr_db=18,
            modulation="FHSS", protocol="OcuSync 3.0", freq_hopping=True,
            notes="Latency 28ms. Hỗ trợ chế độ Manual tốc độ cao."),

        UAV(name="Parrot ANAFI USA",
            manufacturer="Parrot", model="ANAFI USA", category="Military",
            year=2020, weight_g=500, max_speed_kmh=55, max_altitude_m=4755,
            flight_time_min=32, range_km=5, battery_mah=3400,
            freq_center_mhz=5150, freq_bandwidth_mhz=80, snr_db=19,
            modulation="OFDM", protocol="Proprietary AES-256", freq_hopping=True,
            notes="Được sử dụng bởi quân đội Mỹ. Mã hóa AES-256. ITAR compliant."),

        UAV(name="Autel EVO II Pro",
            manufacturer="Autel Robotics", model="EVO II Pro", category="Professional",
            year=2020, weight_g=1191, max_speed_kmh=72, max_altitude_m=7000,
            flight_time_min=40, range_km=9, battery_mah=7100,
            freq_center_mhz=2400, freq_bandwidth_mhz=80, snr_db=21,
            modulation="OFDM", protocol="SkyLink", freq_hopping=True,
            notes="Cảm biến 1 inch, aperture điều chỉnh được f/2.8–f/11."),

        UAV(name="Skydio 2+",
            manufacturer="Skydio", model="2+", category="Professional",
            year=2021, weight_g=800, max_speed_kmh=58, max_altitude_m=4572,
            flight_time_min=27, range_km=9, battery_mah=4280,
            freq_center_mhz=2400, freq_bandwidth_mhz=80, snr_db=18,
            modulation="OFDM", protocol="Skydio Link", freq_hopping=False,
            notes="AI obstacle avoidance 360° với 6 camera 4K. Chuyên theo dõi tự động."),

        UAV(name="Wingtra WingtraOne GEN II",
            manufacturer="Wingtra", model="WingtraOne GEN II", category="Industrial",
            year=2021, weight_g=3700, max_speed_kmh=72, max_altitude_m=4200,
            flight_time_min=59, range_km=60, battery_mah=None,
            freq_center_mhz=900, freq_bandwidth_mhz=20, snr_db=16,
            modulation="FHSS", protocol="MAVLink", freq_hopping=True,
            notes="VTOL fixed-wing. Chuyên khảo sát địa hình, mapping độ chính xác cao."),

        UAV(name="Freefly Alta X",
            manufacturer="Freefly Systems", model="Alta X", category="Industrial",
            year=2019, weight_g=6900, max_speed_kmh=60, max_altitude_m=4000,
            flight_time_min=20, range_km=2, battery_mah=16000,
            freq_center_mhz=2400, freq_bandwidth_mhz=40, snr_db=15,
            modulation="DSSS", protocol="FutabaFASSTest", freq_hopping=False,
            notes="Payload tối đa 15.9 kg. Dùng cho quay phim điện ảnh chuyên nghiệp."),

        UAV(name="Yuneec Typhoon H3",
            manufacturer="Yuneec", model="Typhoon H3", category="Professional",
            year=2019, weight_g=1995, max_speed_kmh=70, max_altitude_m=3000,
            flight_time_min=25, range_km=2, battery_mah=5250,
            freq_center_mhz=2400, freq_bandwidth_mhz=60, snr_db=17,
            modulation="FHSS", protocol="ST16S", freq_hopping=True,
            notes="Hexacopter 6 cánh. Camera Leica joint venture."),

        UAV(name="MQ-9 Reaper",
            manufacturer="General Atomics", model="MQ-9 Reaper", category="Military",
            year=2007, weight_g=4760000, max_speed_kmh=482, max_altitude_m=15240,
            flight_time_min=1080, range_km=1900, battery_mah=None,
            freq_center_mhz=350, freq_bandwidth_mhz=30, snr_db=30,
            modulation="PSK", protocol="Link 16 / SATCOM", freq_hopping=True,
            notes="UCAV quân sự Mỹ. Payload 1.7 tấn vũ khí. SATCOM điều khiển toàn cầu."),

        UAV(name="RQ-4 Global Hawk",
            manufacturer="Northrop Grumman", model="RQ-4B", category="Military",
            year=1998, weight_g=14628000, max_speed_kmh=629, max_altitude_m=18288,
            flight_time_min=2160, range_km=22780, battery_mah=None,
            freq_center_mhz=260, freq_bandwidth_mhz=40, snr_db=32,
            modulation="PSK", protocol="CDL / SATCOM", freq_hopping=True,
            notes="UAV trinh sát tầm cao tầm xa của Không quân Mỹ. ISR nhiệm vụ chiến lược."),

        UAV(name="DJI Agras T40",
            manufacturer="DJI", model="Agras T40", category="Agricultural",
            year=2022, weight_g=24500, max_speed_kmh=21, max_altitude_m=3000,
            flight_time_min=15, range_km=7, battery_mah=29000,
            freq_center_mhz=900, freq_bandwidth_mhz=20, snr_db=18,
            modulation="FHSS", protocol="OcuSync", freq_hopping=True,
            notes="Bình thuốc sâu 40L. Radar tránh chướng ngại vật. Chuyên phun thuốc nông nghiệp."),

        UAV(name="Emlid Reach RX",
            manufacturer="Emlid", model="Reach RX", category="Research",
            year=2022, weight_g=102, max_speed_kmh=0, max_altitude_m=None,
            flight_time_min=None, range_km=None, battery_mah=None,
            freq_center_mhz=1575, freq_bandwidth_mhz=20, snr_db=28,
            modulation="OFDM", protocol="GNSS RTK", freq_hopping=False,
            notes="Module GNSS RTK độ chính xác cm. Thường gắn trên UAV khảo sát."),

        UAV(name="Inspired Flight IF1200A",
            manufacturer="Inspired Flight", model="IF1200A", category="Industrial",
            year=2021, weight_g=5670, max_speed_kmh=72, max_altitude_m=4000,
            flight_time_min=55, range_km=8, battery_mah=22000,
            freq_center_mhz=5800, freq_bandwidth_mhz=80, snr_db=20,
            modulation="OFDM", protocol="DroneSense", freq_hopping=False,
            notes="Octocopter chuyên công nghiệp. Sản xuất tại Mỹ. NDAA compliant."),

        UAV(name="Joby Aviation S4",
            manufacturer="Joby Aviation", model="S4", category="Industrial",
            year=2023, weight_g=1815000, max_speed_kmh=320, max_altitude_m=3000,
            flight_time_min=60, range_km=161, battery_mah=None,
            freq_center_mhz=5030, freq_bandwidth_mhz=100, snr_db=24,
            modulation="OFDM", protocol="UAM Protocol", freq_hopping=True,
            notes="eVTOL taxi bay. FAA certification đang trong quá trình. 5 cánh quạt nghiêng."),

        UAV(name="Zipline P2 Zip",
            manufacturer="Zipline", model="P2 Zip", category="Industrial",
            year=2023, weight_g=8160, max_speed_kmh=129, max_altitude_m=500,
            flight_time_min=None, range_km=16, battery_mah=None,
            freq_center_mhz=915, freq_bandwidth_mhz=25, snr_db=17,
            modulation="FHSS", protocol="Zipline Mesh", freq_hopping=True,
            notes="UAV giao hàng y tế tự động. Hoạt động tại Rwanda, Ghana, Mỹ."),

        UAV(name="Quantum Systems Trinity F90+",
            manufacturer="Quantum Systems", model="Trinity F90+", category="Industrial",
            year=2020, weight_g=3600, max_speed_kmh=108, max_altitude_m=4000,
            flight_time_min=90, range_km=100, battery_mah=None,
            freq_center_mhz=868, freq_bandwidth_mhz=15, snr_db=16,
            modulation="FHSS", protocol="MAVLink 2.0", freq_hopping=True,
            notes="VTOL fixed-wing. Endurance cao nhất phân khúc. Chuyên mapping lớn."),

        UAV(name="Percepto Sparrow",
            manufacturer="Percepto", model="Sparrow", category="Industrial",
            year=2019, weight_g=1800, max_speed_kmh=72, max_altitude_m=3000,
            flight_time_min=30, range_km=5, battery_mah=8000,
            freq_center_mhz=5800, freq_bandwidth_mhz=80, snr_db=19,
            modulation="OFDM", protocol="4G LTE / WiFi", freq_hopping=False,
            notes="Autonomous drone-in-a-box. Tự sạc, tự bay không cần người vận hành."),

        UAV(name="Xiaomi FIMI X8 SE 2022",
            manufacturer="Xiaomi / FIMI", model="X8 SE 2022", category="Consumer",
            year=2022, weight_g=790, max_speed_kmh=68, max_altitude_m=4000,
            flight_time_min=35, range_km=10, battery_mah=4500,
            freq_center_mhz=2400, freq_bandwidth_mhz=60, snr_db=16,
            modulation="FHSS", protocol="FIMI Link", freq_hopping=True,
            notes="Giá thành thấp, cạnh tranh trực tiếp DJI Mini. Camera 4K/100fps."),
    ]
