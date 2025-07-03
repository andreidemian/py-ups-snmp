from .snmp import snmpRead
from .convertTools import (
    convert_centiseconds,
    toFloat
)

class upsAPC(snmpRead):

    def __init__(self, ip:str, port:int = 161, snmpv:int=1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):
        super().__init__(ip, port, snmpv, community, user, authkey, privkey)

    @classmethod
    async def create(cls, ip:str, port:int = 161, snmpv:int=1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):
        return cls(ip, port, snmpv, community, user, authkey, privkey)

    @property
    async def get_name(self) -> str:
        data = await self.get_oid('1.3.6.1.4.1.318.1.1.1.1.1.2.0')
        return data if data else None
    
    @property
    async def get_model(self) -> str:
        data = await self.get_oid('1.3.6.1.4.1.318.1.1.1.1.1.1.0')
        return data if data else None
    
    @property
    async def get_contact(self) -> str:
        data = await self.get_oid('1.3.6.1.2.1.1.4.0')
        return data if data else None
    
    @property
    async def get_location(self) -> str:
        data = await self.get_oid('.1.3.6.1.2.1.1.6.0')
        return data if data else None
    
    @property
    async def get_uioEnvTempP1(self) -> int:
        temp = await self.get_oid('1.3.6.1.4.1.318.1.1.25.1.2.1.6.1.1')
        return int(temp) if temp else None
    
    @property
    async def get_batteryTemperature(self) -> int:
        temp = await self.get_oid('1.3.6.1.4.1.318.1.1.1.2.2.2.0')
        return int(temp) if temp else None

    @property
    async def get_batteryChargePercentage(self) -> int:
        bcp = await self.get_oid('1.3.6.1.4.1.318.1.1.1.2.2.1.0')
        return int(bcp) if bcp else None
    
    @property
    async def get_batteryReplace(self) -> bool:
        br = await self.get_oid('1.3.6.1.4.1.318.1.1.1.2.2.4.0')
        return True if br and int(br) == 2 else False

    @property
    async def get_batteryStatus(self) -> tuple:
        """
            return the battery state and the battery state description
            example all output:
                (1, 'Unknown'),
                (2, 'Normal'),
                (3, 'Low')
        """
        battery_state = { '1': 'Unknown', '2': 'Normal', '3': 'Low', }
        state = await self.get_oid('1.3.6.1.4.1.318.1.1.1.2.1.1.0')
        return (int(state), battery_state[state]) if state else None

    @property
    async def get_batteryRuntime(self) -> dict:
        br = await self.get_oid('1.3.6.1.4.1.318.1.1.1.2.2.3.0')
        return convert_centiseconds(int(br)) if br else None

    @property
    async def get_batteryVoltage(self) -> int:
        obv = await self.get_oid('1.3.6.1.4.1.318.1.1.1.2.2.8.0')
        return int(obv) if obv else None

    @property
    async def get_inputVoltage(self) -> int:
        iv = await self.get_oid('1.3.6.1.4.1.318.1.1.1.3.2.1.0')
        return int(iv) if iv else None
    
    @property
    async def get_inputFrequency(self) -> int:
        inf = await self.get_oid('1.3.6.1.4.1.318.1.1.1.3.2.4.0')
        return int(inf) if inf else None

    @property
    async def get_inputLineFailCause(self) -> tuple:
        """
            return the input status and the input status description
            example all output:
                (1,'noTransfer')
                (2,'highLineVoltage')
                (3,'brownout')
                (4,'blackout')
                (5,'smallMomentarySag')
                (6,'deepMomentarySag')
                (7,'smallMomentarySpike')
                (8,'largeMomentarySpike')
                (9,'selfTest')
                (10,'rateOfVoltageChange')
        """
        ups_state = {
            '1':'noTransfer',
            '2':'highLineVoltage',
            '3':'brownout',
            '4':'blackout',
            '5':'smallMomentarySag',
            '6':'deepMomentarySag',
            '7':'smallMomentarySpike',
            '8':'largeMomentarySpike',
            '9':'selfTest',
            '10':'rateOfVoltageChange'
        }
        state = await self.get_oid('1.3.6.1.4.1.318.1.1.1.3.2.5.0')
        return (int(state), ups_state[state]) if state else None

    @property
    async def get_outputVoltage(self) -> int:
        ouv = await self.get_oid('1.3.6.1.4.1.318.1.1.1.4.2.1.0')
        return int(ouv) if ouv else None
    
    @property
    async def get_outputFrequency(self) -> int:
        ouf = await self.get_oid('1.3.6.1.4.1.318.1.1.1.4.2.2.0')
        return int(ouf) if ouf else None

    @property
    async def get_outputCurrent(self) -> int:
        ouc = await self.get_oid('1.3.6.1.4.1.318.1.1.1.4.2.4.0')
        return int(ouc) if ouc else None
    
    @property
    async def get_baseOutputStatus(self) -> tuple:
        """
         return the UPS state and the UPS state description
         example all output:
            (1, 'unknown'),
            (2, 'onLine'),
            (3, 'onBattery'),
            (4, 'onSmartBoost'),
            (5, 'timedSleeping'),
            (6, 'softwareBypass'),
            (7, 'off'),
            (8, 'rebooting'),
            (9, 'switchedBypass'),
            (10, 'hardwareFailureBypass'),
            (11, 'sleepingUntilPowerReturn'),
            (12, 'onSmartTrim')
        """
        ups_state = {
            '1':'unknown',
            '2':'onLine',
            '3':'onBattery',
            '4':'onSmartBoost',
            '5':'timedSleeping',
            '6':'softwareBypass',
            '7':'off',
            '8':'rebooting',
            '9':'switchedBypass',
            '10':'hardwareFailureBypass',
            '11':'sleepingUntilPowerReturn',
            '12':'onSmartTrim'
        }
        state = await self.get_oid('1.3.6.1.4.1.318.1.1.1.4.1.1.0')
        return (int(state), ups_state[state]) if state else None
    
    @property
    async def get_loadPercentage(self) -> int:
        lper = await self.get_oid('1.3.6.1.4.1.318.1.1.1.4.2.3.0')
        return int(lper) if lper else None

class upsCyberPower(snmpRead):

    def __init__(self, ip:str, port:int = 161, snmpv:int=1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):
        super().__init__(ip, port, snmpv, community, user, authkey, privkey)

    @classmethod
    async def create(cls, ip:str, port:int = 161, snmpv:int= 1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):
        return cls(ip, port, snmpv, community, user, authkey, privkey)

    @property
    async def get_name(self) -> str:
        data = await self.get_oid('.1.3.6.1.2.1.1.5.0')
        return data if data else None

    @property
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
    async def get_serialNumber(self) -> str:
        get_sn = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.1.2.3.0')
        return get_sn if get_sn else None
    
    @property
    async def get_upsTemperature(self) -> int:
        temp = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.10.2.0')
        return int(temp) if temp else None

    @property
    async def get_envTemp(self) -> float:
        str_temp = await self.get_oid('.1.3.6.1.4.1.3808.1.1.4.2.6.0')
        return toFloat(str_temp) if str_temp else None

    @property
    async def get_envHumidity(self) -> int:
        humidity = await self.get_oid('.1.3.6.1.4.1.3808.1.1.4.3.1.0')
        return int(humidity) if humidity else None
    
    @property
    async def get_batteryChargePercentage(self) -> int:
        bcp = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.2.2.1.0')
        return int(bcp) if bcp else None
    
    @property
    async def get_batteryReplace(self) -> bool:
        br = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.2.2.5.0')
        return True if br and int(br) == 2 else False

    @property
    async def get_batteryStatus(self) -> tuple:
        """
            return the battery state and the battery state description
            example all output:
                (1, 'Unknown'),
                (2, 'Normal'),
                (3, 'Low')
        """
        battery_state = { '1': 'Unknown', '2': 'Normal', '3': 'Low', }
        state = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.2.1.1.0')
        return (int(state), battery_state[state]) if state else None

    @property
    async def get_batteryRuntime(self) -> str:
        br = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.2.2.4.0')
        return convert_centiseconds(int(br)) if br else None

    @property
    async def get_batteryVoltage(self) -> float:
        obv = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.2.2.2.0')
        return toFloat(obv) if obv else None

    @property
    async def get_inputVoltage(self) -> float:
        iv = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.3.2.1.0')
        return toFloat(iv) if iv else None
    
    @property
    async def get_inputFrequency(self) -> float:
        inf = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.3.2.4.0')
        return toFloat(inf) if inf else None

    @property
    async def get_inputLineFailCause(self) -> tuple:
        """
            return the input status and the input status description
            example all output:
                (1, 'Normal'),
                (2, 'Over Voltage'),
                (3, 'Under Voltage'),
                (4, 'Frequency Failure'),
                (5, 'Blackout')
        """
        ups_state = { '1': 'Normal', '2': 'Over Voltage', '3': 'Under Voltage', '4': 'Frequency Failure', '5': 'Blackout' }
        state = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.3.2.6.0')
        return (int(state), ups_state[state]) if state else None

    @property
    async def get_inputTransferReason(self) -> int:
        """
            return the input transfer reason and the input transfer reason description
            example all output:
                (1, 'No Transfer'),
                (2, 'High Voltage'),
                (3, 'Brownout'),
                (4, 'Self Test')
        """
        transfer_reason = { '1': 'No Transfer', '2': 'High Voltage', '3': 'Brownout', '4': 'Self Test' }
        state = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.3.2.5.0')
        return (int(state), transfer_reason[state]) if state else None

    @property
    async def get_outputVoltage(self) -> float:
        ouv = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.4.2.1.0')
        return toFloat(ouv) if ouv else None
    
    @property
    async def get_outputFrequency(self) -> float:
        ouf = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.4.2.2.0')
        return toFloat(ouf) if ouf else None

    @property
    async def get_outputCurrent(self) -> float:
        ouc = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.4.2.4.0')
        return toFloat(ouc) if ouc else None
    
    @property
    async def get_outputWattage(self) -> int:
        ouw = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.4.2.5.0')
        return int(ouw) if ouw else None

    @property
    async def get_baseOutputStatus(self) -> tuple:
        """
         return the UPS state and the UPS state description
         example all output: 
            (1, 'Unknown'),
            (2, 'Online'), 
            (3, 'On Battery'), 
            (4, 'On Boost'), 
            (5, 'On Sleep'), 
            (6, 'Off'), 
            (7, 'Rebooting')
        """
        ups_state = { '1': 'Unknown','2': 'Online','3': 'On Battery','4': 'On Boost','5': 'On Sleep','6': 'Off','7': 'Rebooting' }
        state = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.4.1.1.0')
        return (int(state), ups_state[state]) if state else None
    
    @property
    async def get_loadPercentage(self) -> int:
        lper = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.4.2.3.0')
        return int(lper) if lper else None
    
    @property
    async def get_powerRating(self) -> int:
        upr = await self.get_oid('.1.3.6.1.4.1.3808.1.1.1.1.2.6.0')
        return int(upr) if upr else None