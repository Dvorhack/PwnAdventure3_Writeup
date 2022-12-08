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
        X, Y, Z, look, unk, key = unpack("fffIHH",payload)
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

class PacketShootPayload():
    def __init__(self, payload) :
        self.payload = payload

    @staticmethod
    def parse(payload):
        return PacketShootPayload(payload)
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"Shoot: {self.payload.hex()}"

class ChgmtOutilPayload():
    def __init__(self, nb) :
        self.nb = nb

    @staticmethod
    def parse(payload):
        return ChgmtOutilPayload((payload[0]+1)%10)
    
    def encode(self):
        return self.payload
    
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

@packet_type(0x2a69)
class ShootPacket(Packet):
    TYPE = 0x2a69

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketShootPayload.parse(packet[Packet.HEADER_SIZE:])
        return ShootPacket(header, payload)

def parse(data, port, type):
    pkt = Packet.parse(data)
    # if type == 'client' and pkt.header.type == ShootPacket.TYPE:
    #     print(f"[{port}] {pkt}")
    if type == 'server' and pkt.header.type not in PacketRegistry.TYPE_TO_CLASS:
        print(f"[{port}] {pkt}")

if __name__ == "__main__":
    pkt = Packet.parse(bytes.fromhex("6e76b8001ac75bf6afc66774324589ff02aa00008100"))

    print(pkt)