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
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

seconds = 5
frames = []

for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

stream.stop_stream()
stream.close()
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
