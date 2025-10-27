"""Hash rate calculations for the Miner Pool Stats integration."""

from enum import IntEnum


class HashRateUnit(IntEnum):
    """Enumeration of hash rate units."""

    H = 1
    KH = int(H) * 1000
    MH = int(KH) * 1000
    GH = int(MH) * 1000
    TH = int(GH) * 1000
    PH = int(TH) * 1000
    EH = int(PH) * 1000
    ZH = int(EH) * 1000

    def __str__(self):
        """Return the string representation of the hash rate unit."""

        if self.value == self.KH:
            return "KH/s"
        if self.value == self.MH:
            return "MH/s"
        if self.value == self.GH:
            return "GH/s"
        if self.value == self.TH:
            return "TH/s"
        if self.value == self.PH:
            return "PH/s"
        if self.value == self.EH:
            return "EH/s"
        if self.value == self.ZH:
            return "ZH/s"
        return "H/s"

    @classmethod
    def from_str(cls, value: str):
        """Create a HashRateUnit from a string representation."""

        if value == "KH":
            return cls.KH
        if value == "MH":
            return cls.MH
        if value == "GH":
            return cls.GH
        if value == "TH":
            return cls.TH
        if value == "PH":
            return cls.PH
        if value == "EH":
            return cls.EH
        if value == "ZH":
            return cls.ZH
        return cls.H

    def __repr__(self):
        """Return a string representation of the hash rate unit."""

        return str(self)

    def model_dump(self):
        """Return a dictionary representation of the hash rate unit."""

        return {"value": self.value, "suffix": str(self)}


class HashRate:
    """Class to represent a hash rate value with a unit."""

    def __init__(self, value: float, unit: HashRateUnit) -> None:
        """Initialize a HashRate instance with a value and unit."""
        self.value = value
        self.unit = unit

    @classmethod
    def from_known_number(cls, value: float, unit: str):
        """Create a HashRate instance from a numeric value and unit string."""

        if unit == "KH":
            return cls(value, HashRateUnit.KH)
        if unit == "MH":
            return cls(value, HashRateUnit.MH)
        if unit == "GH":
            return cls(value, HashRateUnit.GH)
        if unit == "TH":
            return cls(value, HashRateUnit.TH)
        if unit == "PH":
            return cls(value, HashRateUnit.PH)
        if unit == "EH":
            return cls(value, HashRateUnit.EH)
        if unit == "ZH":
            return cls(value, HashRateUnit.ZH)

        return cls(value, HashRateUnit.H)

    @classmethod
    def from_number(cls, value: float):
        """Create a HashRate instance from a numeric value."""

        unit = HashRateUnit.EH  # default to largest unit

        if value < HashRateUnit.KH.value:
            unit = HashRateUnit.H
        elif value < HashRateUnit.MH.value:
            unit = HashRateUnit.KH
        elif value < HashRateUnit.GH.value:
            unit = HashRateUnit.MH
        elif value < HashRateUnit.TH.value:
            unit = HashRateUnit.GH
        elif value < HashRateUnit.PH.value:
            unit = HashRateUnit.TH
        elif value < HashRateUnit.EH.value:
            unit = HashRateUnit.PH

        translated_value = value / unit.value

        return cls(translated_value, unit)

    def to_unit(self, unit: HashRateUnit):
        """Convert the hash rate to a different unit."""

        if self.unit == unit:
            return self

        if self.unit < unit:
            # Convert to a larger unit
            conversion_factor = 1
            for hru in HashRateUnit:
                if hru.value <= self.unit.value:
                    continue
                if hru.value > unit.value:
                    break
                conversion_factor *= 1000

            converted_value = self.value / conversion_factor
        else:
            # Convert to a smaller unit
            conversion_factor = 1
            for hru in reversed(HashRateUnit):
                if hru.value >= unit.value:
                    continue
                if hru.value < self.unit.value:
                    break
                conversion_factor *= 1000

            converted_value = self.value * conversion_factor

        return HashRate(converted_value, unit)

    def __str__(self):
        """Return the string representation of the hash rate."""

        return f"{self.value} {self.unit}"

    def __repr__(self):
        """Return a string representation of the HashRate instance."""

        return f"HashRate(value={self.value}, unit={self.unit})"

    def model_dump(self):
        """Return a dictionary representation of the HashRate instance."""

        return {"value": self.value, "unit": str(self.unit)}
