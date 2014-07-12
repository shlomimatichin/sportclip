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
        subprocess.check_call([
            'ffmpeg', '-i', filename, '-vn', '-ar', '44100', '-ac', '2', '-f', 'wav', waveFilename])
        subprocess.check_call([
            binary, '--input', waveFilename, '--output', pngFilename,
            "--width", str(width), "--height", str(height)])
    finally:
        if eraseWave and os.path.exists(waveFilename):
            os.unlink(waveFilename)


if __name__ == "__main__":
    import sys
    plot(sys.argv[1], 640, 70, "/tmp/out.png")
