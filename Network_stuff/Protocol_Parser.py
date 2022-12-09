from struct import unpack, pack

class PacketRegistry:
    
    TYPE_TO_CLASS = {}

    @staticmethod
    def register(pkt_type, clazz):
        if pkt_type not in PacketRegistry.TYPE_TO_CLASS:
            PacketRegistry.TYPE_TO_CLASS[pkt_type] = clazz
    
    @staticmethod
    def get(pkt_type):
        if pkt_type in PacketRegistry.TYPE_TO_CLASS:
            return PacketRegistry.TYPE_TO_CLASS[pkt_type]
        else:
            return None

class packet_type:
    """
    Class decoraroe to register packet parser/forge classes
    """
    def __init__(self, pkt_type):
        self.pkt_type = pkt_type
    
    def __call__(self, clazz):
        PacketRegistry.register(self.pkt_type, clazz)
        return clazz

class PacketHeader():
    def __init__(self,pkt_hdr = None, type = 0):
        if pkt_hdr is not None:
            self.type = unpack(">H", pkt_hdr)[0]
        else:
            self.type = type

    @staticmethod
    def parse(pkt_hdr):
        type = unpack(">H", pkt_hdr)[0]
        return PacketHeader(type=type)
    
    def encode(self):
        return pack('>H', self.type)
    
    def __str__(self) -> str:
        return f"CMD: 0x{self.type:x}"


class PacketPositionPayload():
    """
    Payload de type Position
    """
    POSITION_SIZE = 20
    def __init__(self, X, Y, Z, look, unk, key):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.look = look
        self.unk = unk
        self.key = key

    @staticmethod
    def parse(payload):
        X, Y, Z, look, unk, key = unpack("fffIHH",payload[:PacketPositionPayload.POSITION_SIZE])
        return PacketPositionPayload(X, Y, Z, look, unk, key)
    
    def encode(self):
        return pack("fffIHH", self.X, self.Y, self.Z, self.look, self.unk, self.key)
    
    def __str__(self) -> str:
        return f"Position packet: {self.X} / {self.Y} / {self.Z} / {self.look}"


class PacketDefaultPayload():
    def __init__(self, payload) :
        self.payload = payload

    @staticmethod
    def parse(payload):
        return PacketDefaultPayload(payload)
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"Unknown payload: {self.payload.hex()}"

class PacketEnemyPosPayload():
    def __init__(self, id, X, Y, Z, payload):
        self.id = id
        self.X = X
        self.Y = Y
        self.Z = Z
        self.payload = payload

    @staticmethod
    def parse(payload):
        id, X, Y, Z= unpack("Ifff",payload[:16])
        return PacketEnemyPosPayload(id, X, Y, Z, payload[16:])
    
    def encode(self):
        return pack("Ifff", self.id, self.X, self.Y, self.Z) + self.payload
    
    def __str__(self) -> str:
        return f"EnemyPos: ID:{self.id} {self.X} / {self.Y} / {self.Z} {self.payload[:10].hex()} ..."

class PacketReloadPayload():
    def __init__(self) :
        self.payload = b''

    @staticmethod
    def parse(payload):
        return PacketReloadPayload()
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"Reload"

class PacketBeaconPayload():
    def __init__(self, payload) :
        self.payload = payload

    @staticmethod
    def parse(payload):
        return PacketBeaconPayload(payload[:35])
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"Beacon: {self.payload.hex()}"

class PacketShootPayload():
    def __init__(self, name_size, name, payload) :
        self.payload = payload
        self.name_size = name_size
        self.name = name

    @staticmethod
    def parse(payload):
        name_size = int.from_bytes(payload[:2], 'little')
        name = ''.join(chr(x) for x in payload[2:2+name_size])
        other = payload[2+name_size:2+name_size+12]
        return PacketShootPayload(name_size,name,other)
    
    def encode(self):
        return self.name_size.to_bytes(2, "little") + self.name.encode() + self.payload
    
    def __str__(self) -> str:
        return f"Shoot Arme:{self.name} Data:{self.payload.hex()}"

class ChgmtOutilPayload():
    def __init__(self, nb) :
        self.nb = nb

    @staticmethod
    def parse(payload):
        return ChgmtOutilPayload((payload[0]+1)%10)
    
    def encode(self):
        return self.nb.to_bytes(1,'big')
    
    def __str__(self) -> str:
        return f"Chgmt outil: {self.nb}"

class JumpPacketPayload():
    def __init__(self, action) :
        self.action = action

    @staticmethod
    def parse(payload):
        if payload[0] == 1:
            return JumpPacketPayload("Monter")
        else:
            return JumpPacketPayload("Descendre")
    
    def encode(self):
        if self.action == "Monter":
            return b'\x01'
        else:
            return b'\x00'
    
    def __str__(self) -> str:
        return f"Jump: {self.action}"

class Packet:
    HEADER_SIZE = 2

    def __init__(self, header, payload):
        self.header = header
        self.payload = payload


    @staticmethod
    def parse( packet):
        header = PacketHeader(packet[:Packet.HEADER_SIZE])
        pkt_clazz = PacketRegistry.get(header.type)
        if pkt_clazz is None:
            return Packet(header, PacketDefaultPayload.parse(packet[Packet.HEADER_SIZE:]))
        else:
            return pkt_clazz.parse(packet)

    def encode(self) -> bytes:
        return self.header.encode() + self.payload.encode()

    def __str__(self):
        return f"{self.header} {self.payload}"


@packet_type(0x6d76)
class PositionPacket(Packet):
    TYPE = 0x6d76

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketPositionPayload.parse(packet[Packet.HEADER_SIZE:])
        return PositionPacket(header, payload)

@packet_type(0x7073)
class EnemyPosPacket(Packet):
    TYPE = 0x7073

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketEnemyPosPayload.parse(packet[Packet.HEADER_SIZE:])
        return EnemyPosPacket(header, payload)

@packet_type(0x1703)
class BeaconPacket(Packet):
    TYPE = 0x1703 

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketBeaconPayload.parse(packet[Packet.HEADER_SIZE:])
        return BeaconPacket(header, payload)

@packet_type(0x6a70)
class JumpPacket(Packet):
    TYPE = 0x6a70

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = JumpPacketPayload.parse(packet[Packet.HEADER_SIZE:])
        return JumpPacket(header, payload)

@packet_type(0x733D)
class ChgmtOutil(Packet):
    TYPE = 0x733D

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = ChgmtOutilPayload.parse(packet[Packet.HEADER_SIZE:])
        return ChgmtOutil(header, payload)

@packet_type(0x726c)
class ReloadPacket(Packet):
    TYPE = 0x726c

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketReloadPayload.parse(packet[Packet.HEADER_SIZE:])
        return ReloadPacket(header, payload)

@packet_type(0x2a69)
class ShootPacket(Packet):
    TYPE = 0x2a69

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketShootPayload.parse(packet[Packet.HEADER_SIZE:])
        return ShootPacket(header, payload)

def parse(data, port, type):
    while len(data) != 0:
        pkt = Packet.parse(data)
        data = data[len(pkt.encode()):]
        # if type == 'client' and pkt.header.type not in PacketRegistry.TYPE_TO_CLASS:
        #     print(f"[{port}] {pkt}")
        if type == 'server' and pkt.header.type != PositionPacket.TYPE:
            print(f"[{port}] {pkt}")

if __name__ == "__main__":
    pkt = Packet.parse(bytes.fromhex("7073a50d0000832c49c6f57402c776b832450000c472000068ff330000007073a60d00002aeac7c5556908c74bb12e450000d4530000b5ff8d0000007073a70d0000addffbc5d99622c727244e450000388a00000000000000007073a80d00004e6108c3099323c75e9a1a450000c03e00000500a00000007073a90d0000767a014547e20bc714aa1145000070d7000057007aff00006d76a20d00003b5fc2c6ea7de3c6241c2545e7fffffffcf17073a30d0000d6b0b1c6f1c2d5c67e382e4500003c800000c0fefeff00007073a40d000006c5cbc6984511c7a27e43450000e9b80000e4ff62ff00000000"))

    print(pkt)
