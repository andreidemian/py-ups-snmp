from .snmp import snmpRead
from .snmpMibMapping import ( 
    get_iftype_description,
    get_ifOperStatus_description,
    get_ifAdminStatus_description
)

class host(snmpRead):
    """
    SNMP Host Defaults
    """


    def __init__(self,ip: str,port: int = 161,snmpv: int = 1,community: str = None,user: str = None,authkey: str = None,privkey: str = None):
        super().__init__(ip, port, snmpv, community, user, authkey, privkey)


    @classmethod
    async def create(cls,ip: str,port: int = 161,snmpv: int = 1,community: str = None,user: str = None,authkey: str = None,privkey: str = None):
        """
        Create an SNMP object asynchronously.
        """
        return cls(ip, port, snmpv, community, user, authkey, privkey)


    @property
    async def get_hostName(self) -> str:
        hostname = await self.get_oid(".1.3.6.1.2.1.1.5.0")
        return str(hostname) if hostname != None else None


    @property
    async def get_contact(self) -> str:
        contact = await self.get_oid(".1.3.6.1.2.1.1.4.0")
        return str(contact) if contact != None else None


    @property
    async def get_location(self) -> str:
        location = await self.get_oid(".1.3.6.1.2.1.1.6.0")
        return str(location) if location != None else None


    @property
    async def get_upTime(self) -> str:
        uptime = await self.get_oid(".1.3.6.1.2.1.1.3.0")
        return str(uptime) if uptime != None else None


    # System Metrics
    @property
    async def get_memSwapMetrics(self) -> dict:
        """
        Memory Swap Metrics
        """
        mem = {}
        # Swap Memory Statistics
        ## Total swap space available on the system (in KB).
        memTotalSwap = await self.get_oid(".1.3.6.1.4.1.2021.4.3.0")
        mem['memTotalSwap'] = int(memTotalSwap) if memTotalSwap != None else None
        ## Currently available swap space (not used).
        memAvailSwap = await self.get_oid(".1.3.6.1.4.1.2021.4.4.0")
        mem['memAvailSwap'] = int(memAvailSwap) if memAvailSwap != None else None
        ## Minimum required swap space before alerting (in KB).
        memMinimumSwap = await self.get_oid(".1.3.6.1.4.1.2021.4.12.0")
        mem['memMinimumSwap'] = int(memMinimumSwap) if memMinimumSwap != None else None
    
        return mem


    @property
    async def get_memMetrics(self) -> dict:
        """
        Memory Metrics
        """
        mem = {}
        # Physical (Real) Memory (RAM) Statistics
        ## Total RAM available on the system (in KB).
        memTotalReal = await self.get_oid(".1.3.6.1.4.1.2021.4.5.0")
        mem['memTotalReal'] = int(memTotalReal) if memTotalReal != None else None
        ## Total RAM used on the system (in KB).
        memAvailReal = await self.get_oid(".1.3.6.1.4.1.2021.4.6.0")
        mem['memAvailReal'] = int(memAvailReal) if memAvailReal != None else None
        ## Total RAM free on the system (in KB).
        memTotalReal = await self.get_oid(".1.3.6.1.4.1.2021.4.11.0")
        mem['memTotalFree'] = int(memTotalReal) if memTotalReal != None else None

        # Memory Buffers
        ## Shared memory used by multiple processes
        memShared = await self.get_oid(".1.3.6.1.4.1.2021.4.13.0")
        mem['memShared'] = int(memShared) if memShared != None else None
        ## Buffer memory used for temporary data.
        memBuffer = await self.get_oid(".1.3.6.1.4.1.2021.4.14.0")
        mem['memBuffer'] = int(memBuffer) if memBuffer != None else None
        ## Cached memory (used for speeding up file access).
        memCached = await self.get_oid(".1.3.6.1.4.1.2021.4.15.0")
        mem['memCached'] = int(memCached) if memCached != None else None
                                            
        return mem


    @property
    async def get_cpuMetrics(self) -> dict:
        """
        CPU Metrics
        """
        cpu = {}
        # CPU Utilization (Percentage)
        ## Percentage of CPU time spent in user mode (processing applications)
        ssCpuUser = await self.get_oid(".1.3.6.1.4.1.2021.11.9.0")
        cpu['ssCpuUser'] = int(ssCpuUser) if ssCpuUser != None else None
        ## Percentage of CPU time spent in system mode (kernel operations)
        ssCpuSystem = await self.get_oid(".1.3.6.1.4.1.2021.11.10.0")
        cpu['ssCpuSystem'] = int(ssCpuSystem) if ssCpuSystem != None else None
        ## Percentage of CPU time the system is idle.
        ssCpuIdle = await self.get_oid(".1.3.6.1.4.1.2021.11.11.0")
        cpu['ssCpuIdle'] = int(ssCpuIdle) if ssCpuIdle != None else None

        # CPU & Interrupts
        ## interrupts per second
        ssSysInterrupts = await self.get_oid(".1.3.6.1.4.1.2021.11.7.0")
        cpu['ssSysInterrupts'] = int(ssSysInterrupts) if ssSysInterrupts != None else None
        ## context switches per second
        ssSysContext = await self.get_oid(".1.3.6.1.4.1.2021.11.8.0")
        cpu['ssSysContext'] = int(ssSysContext) if ssSysContext != None else None

        return cpu


    @property
    async def get_LoadAvg(self) -> list[float]:
        """
        Load Average
        """
        load_avg = {}
        # load average in 1 minute
        load_avg1 = await self.get_oid(".1.3.6.1.4.1.2021.10.1.3.1")
        load_avg['load_avg1'] = float(load_avg1) if load_avg1 != None else None
        # load average in 5 minutes
        load_avg5 = await self.get_oid(".1.3.6.1.4.1.2021.10.1.3.2")
        load_avg['load_avg5'] = float(load_avg5) if load_avg5 != None else None
        # load average in 15 minutes
        load_avg15 = await self.get_oid(".1.3.6.1.4.1.2021.10.1.3.3")
        load_avg['load_avg15'] = float(load_avg15) if load_avg15 != None else None

        return load_avg


    @property
    async def get_storage(self) -> list[dict]:
        """
        Storage usage metrics (Disk)
        """
        
        storage_root_oid = '.1.3.6.1.2.1.25.2.3.1'
        storage_index = await self.walk_oid(f"{storage_root_oid}.1")

        if not storage_index:
            return None
        
        storages = []
        for oid, id in storage_index:
            
            storage = {}

            # Storage type
            storage_type = await self.get_oid(f"{storage_root_oid}.2.{id}")

            if not storage_type:
                continue

            # only hrStorageFixedDisk type
            if storage_type == '1.3.6.1.2.1.25.2.1.4':
                # The index of the storage area on the device.
                storage['Index'] = int(id)
                # The name of the storage area.
                desc = await self.get_oid(f"{storage_root_oid}.3.{id}")
                storage['Descr'] = str(desc) if desc != None else None
                # The size of the storage area.
                AllocationUnits = await self.get_oid(f"{storage_root_oid}.4.{id}")
                storage['AllocationUnits'] = int(AllocationUnits) if AllocationUnits != None else None
                # The total size of the storage area.
                Size = await self.get_oid(f"{storage_root_oid}.5.{id}")
                storage['Size'] = int(Size) if Size != None else None
                # The amount of the storage area that is currently in use.
                Used = await self.get_oid(f"{storage_root_oid}.6.{id}")
                storage['Used'] = int(Used) if Used != None else None

                # The percentage of the storage area that is currently in use.
                storage['UsedPercent'] = round((storage['Used'] / storage['Size'] * 100),2) if storage['Used'] != None and storage['Size'] != None else None
                # The percentage of the storage area that is currently available.
                storage['FreePercent'] = round((100 - storage['UsedPercent']),2) if storage['UsedPercent'] != None else 0.0

                storages.append(storage)
            
        storages.sort(key=lambda x: x['Index'])
        return storages


    # Disk IO Metrics
    @property
    async def get_diskION(self) -> list[dict]:
        """
        Disk I/O Operations Metrics (Bytes)
        """
        disk_root_oid = ".1.3.6.1.4.1.2021.13.15.1.1"
        disk_index = await self.walk_oid(f"{disk_root_oid}.1")

        if not disk_index:
            return None
        
        disks = []
        for oid, id in disk_index:
            disk = {}
            # Represents the index of each disk device in the SNMP table.
            disk['Index'] = int(id)
            # The name of the disk device.
            Device = await self.get_oid(f"{disk_root_oid}.2.{id}")
            disk['Device'] = str(Device) if Device != None else None
            # Total bytes read from each device since boot.
            IONRead = await self.get_oid(f"{disk_root_oid}.3.{id}")
            disk['IONRead'] = int(IONRead) if IONRead != None else None
            # Total bytes written to each device since boot.
            IONWritten = await self.get_oid(f"{disk_root_oid}.4.{id}")
            disk['IONWritten'] = int(IONWritten) if IONWritten != None else None

            disks.append(disk)
        disks.sort(key=lambda x: x['Index'])
        return disks


    @property
    async def get_diskIO(self) -> list[dict]:
        """
        Disk I/O Operations Metrics (Operations)
        """
        disk_root_oid = ".1.3.6.1.4.1.2021.13.15.1.1"
        disk_index = await self.walk_oid(f"{disk_root_oid}.1")

        if not disk_index:
            return None

        disks = []
        for oid, id in disk_index:
            disk = {}
            # Represents the index of each disk device in the SNMP table.
            disk['Index'] = int(id)
            # The name of the disk device.
            Device = await self.get_oid(f"{disk_root_oid}.2.{id}")
            disk['Device'] = str(Device) if Device != None else None
            # Total read operations on each device since boot.
            IOReads = await self.get_oid(f"{disk_root_oid}.5.{id}")
            disk['IOReads'] = int(IOReads) if IOReads != None else None
            # Total write operations on each device since boot.
            IOWrites = await self.get_oid(f"{disk_root_oid}.6.{id}")
            disk['IOWrites'] = int(IOWrites) if IOWrites != None else None

            disks.append(disk)
        disks.sort(key=lambda x: x['Index'])
        return disks


    @property
    async def get_diskIOLA(self) -> list[dict]:
        """
        Disk I/O Load Average
        1, 5, 15 minutes
        """
        disk_root_oid = ".1.3.6.1.4.1.2021.13.15.1.1"
        disk_index = await self.walk_oid(f"{disk_root_oid}.1")

        if not disk_index:
            return None

        disks = []
        for oid, id in disk_index:
            disk = {}
            # Represents the index of each disk device in the SNMP table.
            disk['Index'] = int(id)
            # The name of the disk device.
            Device = await self.get_oid(f"{disk_root_oid}.2.{id}")
            disk['Device'] = str(Device) if Device != None else None
            # These values represent disk utilization over 1, 5, and 15 minutes, similar to CPU load averages.
            iola1 = await self.get_oid(f"{disk_root_oid}.9.{id}")
            disk['IOLA1'] = int(iola1) if iola1 != None else None
            iola5 = await self.get_oid(f"{disk_root_oid}.10.{id}")
            disk['IOLA5'] = int(iola5) if iola5 != None else None
            iola15 = await self.get_oid(f"{disk_root_oid}.11.{id}")
            disk['IOLA15'] = int(iola15) if iola15 != None else None

            disks.append(disk)
        disks.sort(key=lambda x: x['Index'])
        return disks


    @property
    async def get_diskIONX(self) -> list[dict]:
        """
        Disk I/O Operations Metrics (Extended)
        """
        disk_root_oid = ".1.3.6.1.4.1.2021.13.15.1.1"
        disk_index = await self.walk_oid(f"{disk_root_oid}.1")

        if not disk_index:
            return None
        
        disks = []
        for oid, id in disk_index:
            disk = {}
            # Represents the index of each disk device in the SNMP table.
            disk['Index'] = int(id)
            # The name of the disk device.
            Device = await self.get_oid(f"{disk_root_oid}.2.{id}")
            disk['Device'] = str(Device) if Device != None else None
            # The diskIONReadX and diskIONWrittenX variables represent extended versions of the diskIONRead and diskIONWritten variables.
            IONReadX = await self.get_oid(f"{disk_root_oid}.12.{id}")
            disk['IONReadX'] = int(IONReadX) if IONReadX != None else None
            IONWrittenX = await self.get_oid(f"{disk_root_oid}.13.{id}")
            disk['IONWrittenX'] = int(IONWrittenX) if IONWrittenX != None else None

            disks.append(disk)
        disks.sort(key=lambda x: x['Index'])
        return disks


    # SNMP Sensors
    @property
    async def get_sensors(self) -> list[dict]:
        """
        SNMP Sensors
        """
        # The OID prefix for the sensor table
        sensor_root_oid = ".1.3.6.1.4.1.2021.13.16.2.1"
        sensor_indices = await self.walk_oid(f"{sensor_root_oid}.1")

        if not sensor_indices:
            return None
        
        sensors = []
        for oid, id in sensor_indices:
            sensor = {}
            sensor['Index'] = int(id)
            descr = await self.get_oid(f"{sensor_root_oid}.2.{id}")
            sensor['Sensor'] = str(descr) if descr != None else None
            s_value = await self.get_oid(f"{sensor_root_oid}.3.{id}")
            sensor['Value'] = (int(s_value) / 1000.0) if s_value != None else None

            sensors.append(sensor)

        sensors.sort(key=lambda x: x['Index'])
        return sensors