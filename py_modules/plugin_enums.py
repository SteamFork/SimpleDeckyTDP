from enum import Enum

class GpuModes(Enum):
  FIXED = "FIXED"
  BATTERY = "BATTERY"
  BALANCE = "BALANCE"
  PERFORMANCE = "PERFORMANCE"

class GpuRange(Enum):
  MIN = "minGpuFrequency"
  MAX = "maxGpuFrequency"
  FIXED = "fixedGpuFrequency"
