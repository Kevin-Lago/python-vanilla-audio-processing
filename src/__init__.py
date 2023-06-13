"""Just another project"""
from pedalboard import Pedalboard, Reverb, NoiseGate, Compressor, LowShelfFilter, Gain, Distortion, PitchShift, HighShelfFilter
from pedalboard.io import AudioStream
import pyaudio

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
        print("Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


def main():
    print()
    with AudioStream(
        input_device_name="Focusrite USB (Focusrite USB Audio)",
        output_device_name="Speakers (Logitech PRO X Gaming Headset)",
        allow_feedback=True
    ) as stream:
        stream.plugins = Pedalboard([
            Distortion(),
            LowShelfFilter(cutoff_frequency_hz=80, gain_db=10, q=1),
            HighShelfFilter(cutoff_frequency_hz=180, gain_db=.2),
            NoiseGate(threshold_db=-40, ratio=1.5, release_ms=250),
            Gain(gain_db=6),
            Compressor(threshold_db=-20, ratio=25),
        ])
        input("Press enter to stop streaming...")


if __name__ == '__main__':
    main()
