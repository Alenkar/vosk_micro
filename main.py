import json
import queue

from vosk import Model, KaldiRecognizer
from vosk import GpuInit, GpuThreadInit
import sounddevice as sd


# Получение информации о микрофоне
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])


GpuInit()
GpuThreadInit()

# Подготовка модели
model = Model("model/vosk-model-small-ru-0.22")
# model = Model("model/vosk-model-ru-0.42")
recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)

q = queue.Queue()

# Чтение корпуса слов
with open("data/obscene_corpus.txt", 'r') as file:
    word_list = file.read().splitlines()


def recordCallback(indata, frames, time, status):
    q.put(bytes(indata))


temp_partial_result = ""
# with sd.RawInputStream(dtype='int16', channels=1, callback=recordCallback, latency=0.25):
with sd.RawInputStream(
        dtype='int16', samplerate=samplerate, blocksize=2000, channels=1, callback=recordCallback):
    print("Start Recognized")
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            # Вывод полного результата
            text = json.loads(recognizer.Result())["text"]
            if len(text) == 0:
                continue
            print(f"Text: {text}")
            text_arr = text.split()
            check = any(text_arr.count(item) for item in word_list)
            if check:
                print("Obscene checked!")
            print("\n")
        else:
            # Вывод промежуточного результата
            partial_result = json.loads(recognizer.PartialResult())["partial"]
            if len(partial_result) != 0 and temp_partial_result != partial_result:
                print(f"Partial result: {partial_result}")
            temp_partial_result = partial_result
