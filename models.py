import asyncio
import subprocess
from viam.components.sensor import Sensor
from viam.proto.app.robot import ComponentConfig
from typing import Mapping, Self
from viam.module.module import Module
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
import smbus2

from viam import logging

LOGGER = logging.getLogger(__name__)

class i2cdetect(Sensor, EasyResource):
    MODEL = "michaellee1019-2:i2cdetect-renamed:i2cdetect"
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

def check_and_enable_i2c():
    try:
        # Check the current I2C configuration
        result = subprocess.run(
            ["sudo", "raspi-config", "nonint", "get_i2c"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Get the returned output and strip any whitespace
        i2c_status = result.stdout.strip()

        # If the status is 1, enable I2C
        if i2c_status == "1":
            LOGGER.info("I2C is disabled. Enabling it now...")
            subprocess.run(
                ["sudo", "raspi-config", "nonint", "do_i2c", "0"], check=True
            )
            LOGGER.info("I2C has been enabled.")
        else:
            LOGGER.info("I2C is already enabled.")

    except subprocess.CalledProcessError as e:
        LOGGER.error(f"Error executing command: {e}")
        LOGGER.error(f"Output: {e.output}")
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_and_enable_i2c()
    asyncio.run(Module.run_from_registry())