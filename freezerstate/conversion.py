import freezerstate.config

class Conversion:

    @staticmethod
    def TemperatureString(temperature, units, includeUnits = False):

        if (includeUnits is True):
            return f'{UnitizedTemperature(temperature, units)}{UnitString(units)}'

        return f'{UnitizedTemperature(temperature, units)}'

    @staticmethod
    def UnitizedTemperature(temperature, units):
        if (units != 'farenheit'):
            return temperature

        farenheit = round((temperature * 1.8) + 32.0, 1)
        return farenheit

    @staticmethod
    def UnitString(units):
        unit_conversion = ({
            'celsius': ('C'),
            'farenheit': ('F')
        })

        unitvalue = unit_conversion[units]
        return unitvalue
