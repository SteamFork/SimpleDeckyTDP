from enum import Enum

class GpuModes(Enum):
  BALANCE = "BALANCE"
  PERFORMANCE = "PERFORMANCE"
  BATTERY = "BATTERY"
  FIXED = "FIXED"

class GpuRange(Enum):
  MIN = "minGpuFrequency"
  MAX = "maxGpuFrequency"
  FIXED = "fixedGpuFrequency"
