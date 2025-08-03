from pydub import AudioSegment
sound = AudioSegment.from_file("sound/tap.wav")
sound = sound.set_frame_rate(44100).set_channels(2)
sound.export("sound/tap_fixed.wav", format="wav")