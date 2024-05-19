# michaellee1019:i2cdetect
A Viam module that returns all active i2c addresses as sensor values. Useful for troubleshooting wiring and connection issues without having to install software or SSH into the device.

# Attributes
Specifying an `i2c_bus` attribute is required.

```json
{
  "i2c_bus": 1,
}
```

# GetReadings
The Sensor.GetReadings response will look like the following. It will list the hexidecimal i2c address of each device that is communicating over the i2c bus. Note that the api call will trigger a read from devices at all addresses on the bus. It could have unindended consequences for devices that perform operations during a read, but is generally safe.

```json
	
{
  "active": [
    "0x68"
  ]
}

```
