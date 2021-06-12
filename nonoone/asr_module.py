import speech_recognition as sr
'''
pip install SpeechRecognition
pip install pyaudio

'''
r = sr.Recognizer()

# path = './data/R052.wav'
path = './data/R054.wav'
# path = './data/19133.wav'
# path = './data/28_027.wav'

def _recognition_input(path='./data/28_027.wav'):
    '''
    Using google api for recognize speech and return a text describe input file.
    Language : vietnamese
    :param path: path to raw audio file
    :return: text - The output is the recognized text
    '''

    with sr.WavFile(path) as source:
        audio = r.record(source)

    try:
        tmp = r.recognize_google(audio, language='vi-VN')
        return tmp
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return None

tmp = _recognition_input(path=path)
print(tmp)
