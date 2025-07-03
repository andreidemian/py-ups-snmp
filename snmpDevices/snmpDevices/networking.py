from .snmp import snmpRead
from .snmpMibMapping import ( 
    get_iftype_description,
    get_ifOperStatus_description,
    get_ifAdminStatus_description
)
import asyncio

class ifaceMetrics(snmpRead):
    """
    Interface Metrics Class ISO/IEC 8802-3 (Ethernet)
    """


    def __init__(self,ip: str,port: int = 161,snmpv: int = 1,community: str = None,user: str = None,authkey: str = None,privkey: str = None):
        super().__init__(ip, port, snmpv, community, user, authkey, privkey)
        self.if_root_oid = ".1.3.6.1.2.1.2.2.1"
        self.list_of_interfaces_cache = []


    async def async_init(self):
        return await self.walk_oid(f"{self.if_root_oid}.1")


    async def get_interface_descrition(self, id: int) -> dict:
        """
        Get the description of the interface.
        """
        descr = await self.get_oid(f"{self.if_root_oid}.2.{id}")
        self.list_of_interfaces_cache.append({
            "index":id,
            "descr":str(descr) if descr else None
        })
        self.list_of_interfaces_cache.sort(key=lambda x: x['index'])
        return self


    @classmethod
    async def create(cls, ip: str, port: int = 161, snmpv: int = 1, community: str = None, user: str = None, authkey: str = None, privkey: str = None):
        """ 
            Create an instance of the ifaceMetrics class and initialize it.
        """
        instance = cls(ip, port, snmpv, community, user, authkey, privkey)

        for oid, id in await instance.async_init():
            await instance.get_interface_descrition(int(id))
        return instance


    def __iter__(self):
        return iter(self.list_of_interfaces_cache)


    # Interface Metrics
    async def get_ifType(self,int_index:int) -> dict:
        """
        Interface Type  (Ethernet, Loopback, etc.)
        """
        # The type of interface.
        type = await self.get_oid(f"{self.if_root_oid}.3.{int_index}")
        return get_iftype_description(int(type)) if type != None else None


    async def get_ifMtu(self,int_index:int) -> dict:
        """
        Interface MTU (Maximum Transmission Unit)
        """
        # The size of the largest packet that can be sent/received on the interface.
        mtu = await self.get_oid(f"{self.if_root_oid}.4.{int_index}")
        return int(mtu) if mtu != None else None


    async def get_ifSpeed(self,int_index:int) -> dict:
        """
        Interface Speed (bits per second)
        """
        # The speed of the interface in bits per second.
        speed = await self.get_oid(f"{self.if_root_oid}.5.{int_index}")
        return int(speed) if speed != None else None


    async def get_ifHighSpeed(self,int_index:int) -> dict:
        """
        Interface Speed (bits per second)
        """
        # The speed of the interface in bits per second.
        speed = await self.get_oid(f".1.3.6.1.2.1.31.1.1.1.15.{int_index}")
        return int(speed) if speed != None else None


    async def get_ifPhysAddress(self,int_index:int) -> dict:
        """
        Interface Physical Address (MAC Address)
        """

        # The interface's address at the protocol layer immediately 'below' the network layer in the protocol stack.
        PhysAddress = str(await self.get_oid(f"{self.if_root_oid}.6.{int_index}"))
        if PhysAddress:
            return (":".join([PhysAddress[i:i+2] for i in range(0, len(PhysAddress), 2)])).replace("0x:", "")
        return None


    async def get_ifAdminStatus(self,int_index:int) -> dict:
        """
        Interface Admin Status (Up, Down)
        The current operational state of the interface
        """

        # The current operational state of the interface.
        AdminStatus = await self.get_oid(f"{self.if_root_oid}.7.{int_index}")
        return get_ifAdminStatus_description(int(AdminStatus)) if AdminStatus != None else None


    async def get_ifOperStatus(self,int_index:int) -> dict:
        """
        Interface Operational Status (Up, Down)
        """

        # The current operational state of the interface.
        OperStatus = await self.get_oid(f"{self.if_root_oid}.8.{int_index}")
        return get_ifOperStatus_description(int(OperStatus)) if OperStatus != None else None


    async def get_ifLastChange(self,int_index:int) -> dict:
        """
        Interface Last Change
        """

        # The value of sysUpTime at the time the interface entered its current operational state.
        LastChange = await self.get_oid(f"{self.if_root_oid}.9.{int_index}")
        return int(LastChange) if LastChange != None else None


    async def get_ifIOOctets(self,int_index:int) -> dict:
        """
        Interface I/O Octets (Bytes)
        """

        # The total number of octets received on the interface, including framing characters.
        InOctets = await self.get_oid(f"{self.if_root_oid}.10.{int_index}")
        
        # The total number of octets transmitted out of the interface, including framing characters.
        OutOctets = await self.get_oid(f"{self.if_root_oid}.16.{int_index}")

        return {
            "in": int(InOctets) if InOctets != None else None,
            "out": int(OutOctets) if OutOctets != None else None
        }


    async def get_ifHCIOOctets(self,int_index:int) -> dict:
        """
        Interface I/O Octets (High Capacity 64bit) (Bytes)
        """

        # The total number of octets received on the interface, including framing characters.
        InOctets = await self.get_oid(f".1.3.6.1.2.1.31.1.1.1.6.{int_index}")

        # The total number of octets transmitted out of the interface, including framing characters.
        OutOctets = await self.get_oid(f".1.3.6.1.2.1.31.1.1.1.10.{int_index}")
        
        return {
            "in": int(InOctets) if InOctets != None else None,
            "out": int(OutOctets) if OutOctets != None else None
        }


    async def get_ifIOErrors(self,int_index:int) -> dict:
        """
        Interface I/O Errors
        """

        # The number of inbound packets that contained errors preventing them from being deliverable to a higher-layer protocol.
        InErrors = await self.get_oid(f"{self.if_root_oid}.14.{int_index}")

        # The number of outbound packets that could not be transmitted because of errors.
        OutErrors = await self.get_oid(f"{self.if_root_oid}.20.{int_index}")

        return {
            "in": int(InErrors) if InErrors != None else None,
            "out": int(OutErrors) if OutErrors != None else None
        }


    async def get_ifIODiscards(self,int_index:int) -> dict:
        """
        Interface Discards
        """

        # The number of inbound packets which were chosen to be discarded even though no errors had been detected to prevent their being delivered.
        InDiscards = await self.get_oid(f"{self.if_root_oid}.13.{int_index}")

        # The number of outbound packets which were chosen to be discarded even though no errors had been detected to prevent their being transmitted.
        OutDiscards = await self.get_oid(f"{self.if_root_oid}.19.{int_index}")

        return {
            "in": int(InDiscards) if InDiscards != None else None,
            "out": int(OutDiscards) if OutDiscards != None else None
        }


    async def get_ifUnknownProtos(self,int_index:int) -> dict:
        """
        Interface Unknown Protocols
        """

        # The number of packets received via the interface which were discarded because of an unknown or unsupported protocol.
        InUnknownProtos = await self.get_oid(f"{self.if_root_oid}.15.{int_index}")

        return int(InUnknownProtos) if InUnknownProtos != None else None


    async def get_ifNUcastPkts(self,int_index:int) -> dict:
        """
        Interface Inbound Non-Unicast Packets
        """

        # The number of packets, delivered by this sub-layer to a higher (sub-)layer, which were addressed to a multicast address at this sub-layer.
        InNUcastPkts = await self.get_oid(f"{self.if_root_oid}.12.{int_index}")

        # The total number of packets that higher-level protocols requested be transmitted to a sub-layer (i.e., the number of packets passed to the MAC service provider).
        OutNUcastPkts = await self.get_oid(f"{self.if_root_oid}.18.{int_index}")

        return {
            "in": int(InNUcastPkts) if InNUcastPkts != None else None,
            "out": int(OutNUcastPkts) if OutNUcastPkts != None else None
        }


    async def get_ifUcastPkts(self,int_index:int) -> dict:
        """
        Interface Inbound Unicast Packets
        """

        # The number of packets, delivered by this sub-layer to a higher (sub-)layer, which were not addressed to a multicast or broadcast address at this sub-layer.
        InUcastPkts = await self.get_oid(f"{self.if_root_oid}.11.{int_index}")
        
        # The total number of packets that higher-level protocols requested be transmitted to a sub-layer (i.e., the number of packets passed to the MAC service provider).
        OutUcastPkts = await self.get_oid(f"{self.if_root_oid}.17.{int_index}")

        return {
            "in": int(InUcastPkts) if InUcastPkts != None else None,
            "out": int(OutUcastPkts) if OutUcastPkts != None else None
        }


    async def get_ifOutQLen(self,int_index:int) -> dict:
        """
        The length of the output packet queue (in packets).
        """

        # The length of the output packet queue (in packets).
        OutQLen = await self.get_oid(f"{self.if_root_oid}.21.{int_index}")
        
        return int(OutQLen) if OutQLen != None else None


    async def get_ifAlias(self,int_index:int) -> dict:
        """
        Interface Alias (Description)
        """

        # The length of the output packet queue (in packets).
        if_alias = await self.get_oid(f".1.3.6.1.2.1.31.1.1.1.18.{int_index}")
        return str(if_alias) if if_alias != None else None


    @property
    async def get_ifIPAddress(self) -> list[dict]:
        """
        Interface IP Address and Netmask
        retruns a list of dictionaries with the following
        index: int
        ipAddress: str
        netaddress: str
        """
        # The index value which uniquely identifies the interface to which this entry is applicable.
        ipAdEntIfIndex_oid = "1.3.6.1.2.1.4.20.1.2"
        ipAdEntIfIndex = await self.walk_oid(ipAdEntIfIndex_oid)

        if not ipAdEntIfIndex:
            return None

        iface_metrics = []
        for ip in ipAdEntIfIndex:
            # The IP address to which this entry's information pertains.
            ifipAddress = str(ip[0][len(ipAdEntIfIndex_oid)+1:]) if ip[0] != None else None
            # The subnet mask associated with the IP address of this entry.
            ifnetmask = str(await self.get_oid(f"1.3.6.1.2.1.4.20.1.3.{ifipAddress}")) if ifipAddress != None else None

            iface_metrics.append(
                {
                    "index": int(ip[1]),
                    "ipAddress": ifipAddress,
                    "netmask": ifnetmask
                }
            )
        return iface_metrics