from functions.run_speech_inference import run_stt
from functions.speech_input import listen


def run_stt_inference():
    listen()
    return run_stt()


if __name__ == '__main__':
    print("Listening...")
    print(run_stt_inference())
