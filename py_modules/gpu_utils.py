import decky_plugin
import glob
import re
import time
import subprocess
from plugin_enums import GpuModes, GpuRange
from plugin_settings import get_saved_settings

GPU_FREQUENCY_PATH = glob.glob("/sys/class/drm/card?/device/pp_od_clk_voltage")[0]
GPU_LEVEL_PATH = glob.glob("/sys/class/drm/card?/device/power_dpm_force_performance_level")[0]

GPU_FREQUENCY_RANGE = None

def get_gpu_frequency_range():
  global GPU_FREQUENCY_RANGE
  if GPU_FREQUENCY_RANGE:
    return GPU_FREQUENCY_RANGE
  try:
    freq_string = open(GPU_FREQUENCY_PATH,"r").read()
    od_sclk_matches = re.findall(r"OD_RANGE:\s*SCLK:\s*(\d+)Mhz\s*(\d+)Mhz", freq_string)

    if od_sclk_matches:
      frequency_range = [int(od_sclk_matches[0][0]), int(od_sclk_matches[0][1])]
      GPU_FREQUENCY_RANGE = frequency_range
      return frequency_range
  except Exception as e:
    decky_plugin.logger.error(e)

def set_gpu_frequency(current_game_id):
  settings = get_saved_settings()
  gpu_mode = GpuModes.DEFAULT.value
  tdp_profile = settings.get("tdpProfiles").get("default")

  if settings.get("enableTdpProfiles"):
    current_tdp_profile = settings.get("tdpProfiles").get(current_game_id)
    if current_tdp_profile:
      tdp_profile = current_tdp_profile
  if tdp_profile.get("gpuMode"):
    gpu_mode = tdp_profile.get("gpuMode")

  # decky_plugin.logger.info(f'{__name__} {current_game_id} {gpu_mode} {tdp_profile}')

  if gpu_mode == GpuModes.DEFAULT.value:
    try:
      # change back to auto
      with open(GPU_LEVEL_PATH,'w') as f:
        f.write("auto")
        f.close()
      return True
    except Exception as e:
      decky_plugin.logger.error(f"{__name__} default mode error {e}")
      return False
  elif gpu_mode == GpuModes.POWERSAVE.value:
    try:
      with open(GPU_LEVEL_PATH,'w') as f:
        f.write("low")
        f.close()
      return True
    except Exception as e:
      decky_plugin.logger.error(f"{__name__} powersaver mode error {e}")
      return False
  elif gpu_mode == GpuModes.RANGE.value:
    new_min = tdp_profile.get(GpuRange.MIN.value, 0)
    new_max = tdp_profile.get(GpuRange.MAX.value, 0)

    return set_gpu_frequency_range(new_min, new_max)
  elif gpu_mode == GpuModes.FIXED.value:
    new_freq = tdp_profile.get(GpuRange.FIXED.value, 0)
    return set_gpu_frequency_range(new_freq, new_freq)
  return True

def set_gpu_frequency_range(new_min: int, new_max: int):
  try:
    min, max = get_gpu_frequency_range()

    # decky_plugin.logger.info(f'{new_min} {new_max}')
    # decky_plugin.logger.info(f'{min} {max}')

    if not (new_min >= min and new_max <= max and new_min <= new_max):
      # invalid values, just change back to auto
      # decky_plugin.logger.info(f'auto')
      if (new_min == 0):
        with open(GPU_LEVEL_PATH,'w') as f:
          f.write("auto")
          f.close()
        return True
      elif (new_min == -1):
        with open(GPU_LEVEL_PATH,'w') as f:
          f.write("low")
          f.close()
        return True
    # decky_plugin.logger.info(f'manual')

    with open(GPU_LEVEL_PATH,'w') as file:
      file.write("manual")
      file.close()
    time.sleep(0.1)
    try:
      execute_gpu_frequency_command(f"s 0 {new_min}")
      execute_gpu_frequency_command(f"s 1 {new_max}")
      execute_gpu_frequency_command("c")
    except Exception as e:
      decky_plugin.logger.error(f"{__name__} error while trying to write frequency range")
    # decky_plugin.logger.info(f'gpu freq range end')

    return True
  except Exception as e:
    decky_plugin.logger.error(f"set_gpu_frequency_range {new_min} {new_max} error {e}")
    return False
  

def execute_gpu_frequency_command(command):
  cmd = f"echo '{command}' | tee {GPU_FREQUENCY_PATH}"
  result = subprocess.run(cmd, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
