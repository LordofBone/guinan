import sounddevice as sd
from scipy.io.wavfile import write

from config.deepspeech import *


def listen():
    """
    Listen to the microphone and return the recorded sound.
    :return:
    """

    fs = 16000
    seconds = 6

    sd.default.samplerate = fs
    sd.default.channels = 1
    sd.default.dtype = "int16"

    audio_in = sd.rec(int(seconds * fs), blocking=True)

    write(str(file_path), fs, audio_in)

    # todo: figure out how to get audio to record only on voice and end when voice is done

    # duration = 5.5  # seconds
    #
    # def callback(indata, outdata, frames, time, status):
    #     if status:
    #         print(status)
    #     print(indata)
    #     outdata[:] = indata
    #
    # with sd.Stream(channels=1, callback=callback):
    #     sd.sleep(int(duration * 1000))


if __name__ == '__main__':
    print(sd.query_devices())
    print(listen())
