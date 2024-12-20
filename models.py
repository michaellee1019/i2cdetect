import viam_wrap
from viam.components.sensor import Sensor
from viam.proto.app.robot import ComponentConfig
from typing import Mapping, Self
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
import sys
import smbus2

class i2cdetect(Sensor):
    MODEL = "michaellee1019:i2cdetect:i2cdetect"
    i2c_bus: int = 1

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        output = self(config.name)
        output.reconfigure(config, dependencies)
        return output

    def reconfigure(self,
                    config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]):
        if config.attributes.fields["i2c_bus"].number_value:
            self.i2c_bus = int(config.attributes.fields["i2c_bus"].number_value)

    async def get_readings(self, **kwargs):
        bus = smbus2.SMBus(self.i2c_bus)
        active = []
        for device in range(128):
            try:
                bus.read_byte(device)
                active.append(hex(device))
            except: # exception if read_byte fails
                pass
        return {"active": active}

if __name__ == '__main__':
    # necessary for pyinstaller to see it
    # build this with: 
    # pyinstaller --onefile --hidden-import viam-wrap --paths $VIRTUAL_ENV/lib/python3.10/site-packages installable.py 
    # `--paths` arg may no longer be necessary once viam-wrap is published somewhere
    # todo: utility to append this stanza automatically at build time
    viam_wrap.main(sys.modules.get(__name__))