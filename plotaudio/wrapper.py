import subprocess
import tempfile
import os


def plot(filename, width, height, pngFilename, waveFilename=None):
    binary = os.path.join(os.path.dirname(__file__), "plotaudio.bin")
    if waveFilename is None:
        waveFilename = tempfile.mktemp(suffix=".wav")
        eraseWave = True
    else:
        eraseWave = False
    try:
        convertToWav(filename, waveFilename)
        subprocess.check_call([
            binary, '--input', waveFilename, '--output', pngFilename,
            "--width", str(width), "--height", str(height)])
    finally:
        if eraseWave and os.path.exists(waveFilename):
            os.unlink(waveFilename)


def convertToWav(original, wave):
    subprocess.check_call([
        ffmpegExecutable(), '-i', original, '-vn', '-ar', '44100',
        '-ac', '2', '-f', 'wav', wave])


def ffmpegExecutable():
    try:
        subprocess.check_output(["which", "ffmpeg"])
        return 'ffmpeg'
    except:
        pass
    try:
        subprocess.check_output(["which", "avconv"])
        return 'avconv'
    except:
        pass
    raise Exception("ffmpeg/avconv not installed")


if __name__ == "__main__":
    import sys
    plot(sys.argv[1], 640, 70, "/tmp/out.png")
