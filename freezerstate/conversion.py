import freezerstate.config

class Conversion:

    def __init__(self):
        self.units = freezerstate.CONFIG.TEMPERATURE_UNITS

    def TemperatureString(self, temperature, includeUnits = False):
        temp = self.UnitizedTemperature(temperature)
        if (includeUnits is True):
            return f'{temp}{self.UnitString()}'

        return f'{temp}'

    def UnitizedTemperature(self, temperature):
        if (self.units != 'farenheit'):
            return temperature

        farenheit = round((temperature * 1.8) + 32.0, 1)
        return farenheit

    def UnitString(self):
        unit_conversion = ({
            'celsius': ('°C'),
            'farenheit': ('°F')
        })

        unitvalue = unit_conversion[self.units]
        return unitvalue