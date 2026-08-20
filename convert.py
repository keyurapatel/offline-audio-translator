from pydub import AudioSegment


def convert_to_wav(input_audio, output_audio):
    audio = AudioSegment.from_file(input_audio)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_audio, format="wav")