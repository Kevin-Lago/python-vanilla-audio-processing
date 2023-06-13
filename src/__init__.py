"""Just another project"""
import wave
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

# Audio signal parameters
# - Number of channels
# - Sample Width
# - Frame rate/Sample Rate
# - Number of Frames
# - Values of a Frame

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
input = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

output = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

seconds = 50
frames = []


def filter_band(data, low, high, m):
    band = list(data)[low:high]

    band = [min(int(x * m), 255) for x in band]

    # butter
    return bytes(band)


def equalizer(data):
    band1 = filter_band(data, 0, 640, 2)
    band2 = filter_band(data, 640, 1280, 2)
    band3 = filter_band(data, 1280, 1920, 2)
    band4 = filter_band(data, 1920, 2560, 2)
    band5 = filter_band(data, 2560, 3200, 2)
    band6 = filter_band(data, 3200, 3840, 0)
    band7 = filter_band(data, 3840, 4480, 0)
    band8 = filter_band(data, 4480, 5120, 0)
    band9 = filter_band(data, 5120, 5760, 0)
    band10 = filter_band(data, 5760, 6400, 0)

    signal = band1 + band2 + band3 + band4 + band5 + band6 + band7 + band8 + band9 + band10
    return signal


for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
    data = input.read(FRAMES_PER_BUFFER)
    out = equalizer(data)
    output.write(out)
    # output.write(data)
    frames.append(data)

input.stop_stream()
input.close()
p.terminate()

obj = wave.open("output.wav", "wb")
obj.setnchannels(CHANNELS)
obj.setsampwidth(p.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b"".join(frames))
obj.close()


def main():
    obj = wave.open("output.wav", "rb")
    print(f"Channels: {obj.getnchannels()}")
    print(f"Sample Width: {obj.getsampwidth()}")
    print(f"Frame Rate: {obj.getframerate()}")
    print(f"# of Frames: {obj.getnframes()}")
    print(obj.getparams())

    sample_freq = obj.getframerate()
    n_samples = obj.getnframes()
    signal_wave = obj.readframes(-1)

    print(type(signal_wave), type(signal_wave[0]))

    t_audio = n_samples / sample_freq

    obj.close()

    signal_array = np.frombuffer(signal_wave, dtype=np.int16)
    times = np.linspace(0, t_audio, num=n_samples)

    plt.figure(figsize=(15, 5))
    plt.plot(times, signal_array)
    plt.title("Kicking It")
    plt.ylabel("Signal Wave")
    plt.xlabel("Time in seconds")
    plt.xlim(0, t_audio)
    plt.show()

    print("blah")


if __name__ == '__main__':
    main()
