import asyncio
from pysnmp.hlapi.asyncio import (
    #getCmd,
    #nextCmd,
    get_cmd,
    next_cmd,
    SnmpEngine, 
    CommunityData, 
    UdpTransportTarget, 
    ContextData, 
    ObjectType, 
    ObjectIdentity, 
    UsmUserData, 
    usmHMACSHAAuthProtocol, 
    usmAesCfb128Protocol
)
import re

class snmpRead:

    """
    SNMP Read class
    """

    def __init__(self, ip:str, port:int = 161, snmpv:int=1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):

        self.ip = ip
        self.port = port
        self.community = community
        self.usm_data = None

        # Set the SNMP version
        if snmpv == 3:
            self.usm_data = UsmUserData(user)
            
            # Set the security level
            if authkey and privkey:
                # If both authKey and privKey are provided, use authPriv security level
                self.usm_data = UsmUserData(
                                user,
                                authKey=authkey,
                                privKey=privkey,
                                authProtocol=usmHMACSHAAuthProtocol,
                                privProtocol=usmAesCfb128Protocol
                        )   
            elif authkey:
                # If only authKey is provided, use authNoPriv security level
                self.usm_data = UsmUserData(
                                user,
                                authKey=authkey,
                                authProtocol=usmHMACSHAAuthProtocol
                            )
            else:
                # If no keys are provided, use noAuthNoPriv security level
                self.usm_data = UsmUserData(user)
        
        SNMP_V_MAP = { 1: 0, 2: 1, 3: 3 }
        self.snmpv = SNMP_V_MAP[snmpv]


    @classmethod
    async def create(cls, ip:str, port:int = 161, snmpv:int=1, community:str=None, user:str=None, authkey:str=None, privkey:str=None):
        """
        Create an instance of the SNMP Read class
        """
        # Create an instance of the class
        return cls(ip, port, snmpv, community, user, authkey, privkey)


    async def run_snmp_get(self, oid: str) -> str:
        """
        SNMP get using getCmd
        """
        # Get the value of the OID
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            SnmpEngine(), # SnmpEngine() is the main object that drives the whole SNMP engine
            self.usm_data if self.snmpv == 3 else CommunityData(self.community, mpModel=self.snmpv),  # model 0 is SNMPv1, model 1 is SNMPv2c
            await UdpTransportTarget.create((self.ip, self.port)), # UdpTransportTarget is the target SNMP entity
            ContextData(), # ContextData() is used to store the SNMP engine's state
            ObjectType(ObjectIdentity(oid)) # ObjectType() is used to represent a MIB object
        )

        # Check for errors and return the value
        if errorIndication:
            print(f"Error Indication: {errorIndication}")
            return None
        # If the value is not found, return None
        elif errorStatus:
            print(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
            return None
        # If the value is found, return it
        else:
            for varBind in varBinds:
                return str(varBind[1].prettyPrint())
        
        return None


    async def run_snmp_get_next(self, oid: str = None) -> tuple:
        """
        SNMP walk using nextCmd
        """
        # Get the next OID
        errorIndication, errorStatus, errorIndex, varBinds = await next_cmd(
            SnmpEngine(), # SnmpEngine() is the main object that drives the whole SNMP engine
            self.usm_data if self.snmpv == 3 else CommunityData(self.community, mpModel=self.snmpv),  # model 0 is SNMPv1, model 1 is SNMPv2c
            await UdpTransportTarget.create((self.ip, self.port)), # UdpTransportTarget is the target SNMP entity
            ContextData(), # ContextData() is used to store the SNMP engine's state
            ObjectType(ObjectIdentity(oid)), # ObjectType() is used to represent a MIB object
            lexicographicMode=False  # Set to False to stop when outside the subtree
        )

        # Check for errors and return the value
        if errorIndication:
            print(f"Error Indication: {errorIndication}")
            return None
        # If the value is not found, return None
        elif errorStatus:
            print(f'Error Status: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
            return None
        # If the value is found, return it
        else:
            for varBind in varBinds:
                return (str(varBind[0]), str(varBind[1]))
        
        return None


    def  match_oid_prefix(self,prefix:str=None, oid:str=None) -> bool:
        """
        Check if the OID matches the prefix
        """

        # Check if the OID matches the prefix
        if(not oid or not prefix):
            return False
        
        # Compile the prefix
        compile = re.compile(f"^{prefix.replace('.', '')}")

        # Check if the OID matches the prefix
        match = compile.match(oid.replace('.', ''))

        if match:
            return True
        
        return False


    async def get_oid(self, oid:str) -> str:
        """
        Get the value of an OID
        """
        return await self.run_snmp_get(oid)


    async def walk_oid(self, root_oid:str=None) -> tuple:
        """
        Walk the SNMP tree starting from root_oid
        """

        # Get the first OID
        data = await self.run_snmp_get_next(root_oid)

        # If the OID is not found, return None
        if(not data):
            return None

        # If the OID is not found, return None
        if(not data[0] and data[1]):
            return (root_oid, data[1])
        
        # If the OID is found, add it to the list
        data_list = []

        # If the OID is found, add it to the list
        if(self.match_oid_prefix(root_oid, data[0])):
            data_list.append(data)
        
        # Walk the tree
        while data[0]:

            # Get the next OID
            data = await self.run_snmp_get_next(data[0])
            if(not self.match_oid_prefix(root_oid, data[0])):
                break

            # If the OID is found, add it to the list
            data_list.append(data)
        
        return data_list