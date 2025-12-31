import numpy as np

SKELS_FILE = r"C:\Users\Gunajothi\OneDrive\Desktop\Pheonix\skels\dev\01April_2010_Thursday_heute-6697.skels"

data = np.loadtxt(SKELS_FILE)

print("Shape:", data.shape)
print("First frame (10 values):", data[0][:10])
print("Mean:", data.mean())
print("Std:", data.std())
