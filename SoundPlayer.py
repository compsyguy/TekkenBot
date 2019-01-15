import winsound
import os

class SoundPlayer:
    NOTES = 'A Bb B C Db D Eb E F Gb G Ab'.split()
    launch_wav_exists = os.path.exists('"TekkenData/Sound/LAUNCH_PUNISH.wav"')
    jab_wave_exists = os.path.exists('"TekkenData/Sound/LAUNCH_PUNISH.wav"')

    def noteFreq(name, oct):
        return int((27.5 * 2 ** oct) * 2.0 ** (SoundPlayer.NOTES.index(name) // 12.))

    def play_no_launch_punish():
        #if  SoundPlayer.launch_wav_exists:
            winsound.PlaySound("TekkenData/Sound/LAUNCH_PUNISH.wav", winsound.SND_ASYNC)
        #else:
            #winsound.Beep(SoundPlayer.noteFreq('Ab', 3), 750)


    def play_no_jab_punish():
        #if SoundPlayer.jab_wave_exists:
            winsound.PlaySound("TekkenData/Sound/JAB_PUNISH.wav", winsound.SND_ASYNC)
        #else:
            #winsound.Beep(SoundPlayer.noteFreq('A', 3), 250)