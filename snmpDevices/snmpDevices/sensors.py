from .snmp import snmpRead
from .convertTools import convert_centiseconds


class HWgSTE(snmpRead):

    def __init__(self, ip:str, port:int = 161, snmpv:int=1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):
        super().__init__(ip, port, snmpv, community, user, authkey, privkey)
    
    @classmethod
    async def create(cls, ip:str, port:int = 161, snmpv:int=1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):
        return cls(ip, port, snmpv, community, user, authkey, privkey)

    @ property
    async def get_name(self) -> str:
        data = await self.get_oid('.1.3.6.1.2.1.1.5.0')
        return data if data else None
    
    @ property
    async def get_model(self) -> str:
        data = await self.get_oid('.1.3.6.1.2.1.1.1.0')
        return data if data else None
    
    @property
    async def get_contact(self) -> str:
        data = await self.get_oid('.1.3.6.1.2.1.1.4.0')
        return data if data else None
    
    @property
    async def get_location(self) -> str:
        data = await self.get_oid('.1.3.6.1.2.1.1.6.0')
        return data if data else None
    
    @property
    async def get_upTime(self) -> str:
        up_time_c = await self.get_oid('.1.3.6.1.2.1.1.3.0')
        return convert_centiseconds(int(up_time_c)) if up_time_c else None
    
    @property
    async def get_ObjectID(self) -> str:
        obj_id = await self.get_oid('.1.3.6.1.2.1.1.2.0')
        return str(obj_id) if obj_id else None

    @property
    async def get_macAddress(self) -> str:
        data = await self.get_oid('.1.3.6.1.4.1.21796.4.1.70.1.0')
        return data if data else None

    @property
    async def get_sensors(self) -> str:
        sensor_name = await self.walk_oid('.1.3.6.1.4.1.21796.4.1.3.1.2')
        sensor_value = await self.walk_oid('.1.3.6.1.4.1.21796.4.1.3.1.4')
        sensor_sn = await self.walk_oid('.1.3.6.1.4.1.21796.4.1.3.1.6')
        sensors = []
        for i, name in enumerate(sensor_name):
            sensors.append({
                name[1]:float(sensor_value[i][1]),
                'sn':sensor_sn[i][1]
            })
        return sensors