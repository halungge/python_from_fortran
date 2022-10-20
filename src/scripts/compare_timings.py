# flake8: noqa D100, D103, E800
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Qt5Agg")
data = np.genfromtxt("cffi_timings.csv", delimiter=",")
fig, axs = plt.subplots(3, 1, sharex=False)
axs[0].plot(data[:, 0], data[:, 1], label="plain cffi")
axs[0].plot(data[:, 0], data[:, 2], label="call_fort_py wrapper")
axs[1].semilogx(data[:, 0], data[:, 1], label="plain cffi")
axs[1].semilogx(data[:, 0], data[:, 2], label="call_fort_py wrapper")
axs[2].bar(data[0:1], data[:, 1])
# axs[2].bar (data[:,0], data[:, 2])
# axs.legend(loc = "upper left")
# axs.set(ylabel='$time [s]$')
plt.show()
