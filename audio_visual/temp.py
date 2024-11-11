import sounddevice as sd
import pandas as pd

# 获取所有设备信息
devices = sd.query_devices()
# print(devices[0])
# 获取所有主机 API 信息
hostapis = sd.query_hostapis()

# 过滤出 hostapi 为 'WASAPI' 的设备
wasapi_devices = [
    device for device in devices
    # if 'WASAPI' in hostapis[device['hostapi']]['name']
]

# 创建一个列表来存储设备信息
device_list = []

# 提取有用的设备信息
for device in wasapi_devices:
    device_info = {
        # 'Device Name': device['name'],
        'Index': device['index'],
        'Host API': hostapis[device['hostapi']]['name'],
        'Max Input Channels': device['max_input_channels'],
        'Max Output Channels': device['max_output_channels'],
        # 'Default Low Input Latency': device['default_low_input_latency'],
        # 'Default Low Output Latency': device['default_low_output_latency'],
        # 'Default High Input Latency': device['default_high_input_latency'],
        # 'Default High Output Latency': device['default_high_output_latency'],
        'Default Samplerate': device['default_samplerate'],
        'Device Name': device['name'],
    }
    device_list.append(device_info)

# 将设备信息转化为 DataFrame
df = pd.DataFrame(device_list)
# df.to_csv('devices_info.txt', sep='\t', index=True)
with open('devices_info.txt', 'w', encoding='utf-8') as f:
    f.write(df.to_string(index=True, justify='center', col_space=15))

print(df)
