from enum import Enum

class GpuModes(Enum):
  DEFAULT = "DEFAULT"
  RANGE = "RANGE"
  FIXED = "FIXED"
  POWERSAVE = "POWERSAVE"

class GpuRange(Enum):
  MIN = "minGpuFrequency"
  MAX = "maxGpuFrequency"
  FIXED = "fixedGpuFrequency"
