import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load("scales4.wav")
y = librosa.util.normalize(y)

y, _ = librosa.effects.trim(y, top_db=30)



onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_frames = librosa.onset.onset_detect(
    y=y,
    sr=sr,
    onset_envelope=onset_env,
    backtrack=True,

    pre_avg=3,
    post_avg=3,
    delta=0.09,
    wait=5
)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
print(onset_times)

S = librosa.stft(y)
S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

iois = np.diff(onset_times)

mean_ioi = np.mean(iois)
std_ioi = np.std(iois)

coefficient_of_variation = std_ioi / mean_ioi

evenness_score = max(0, 100 - np.log1p(coefficient_of_variation) * 100)

print(f"Evenness score: {evenness_score:.2f}/100")
fmin = float(librosa.note_to_hz('C2'))
fmax = float(librosa.note_to_hz('A5'))
print(fmax)

Pxx, freqs, bins, im = plt.specgram(y, NFFT=2048, Fs=sr, noverlap=1024, cmap='magma')

# Set frequency limits
plt.ylim(fmin, fmax)

# Label axes
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.title("Spectrogram Focused on C4 to C6")
plt.colorbar(label='Intensity [dB]')
for onset in onset_times:
    plt.axvline(x=onset, color='cyan', linestyle='--', linewidth=1)
plt.tight_layout()
plt.show()
