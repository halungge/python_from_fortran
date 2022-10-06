import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Qt5Agg")
data = np.genfromtxt("overhead.csv", delimiter=",")
dims1 = data[1:, 0]
width = 0.3  # width of bar
x = np.arange(dims1.shape[0])

x_labels = [str(i) for i in dims1]
pure_overhead = data[1:, 1] / data[1:, 2]
cpy_array = data[1:, 3] / data[1:, 4]

fig, ax = plt.subplots()
ax.bar(x, cpy_array, width, label="array-copy")
ax.bar(x + width + 0.1, pure_overhead, width, label="pure py overhead")
ax.legend()
plt.xticks(ticks=x, labels=x_labels, rotation=45)
plt.xlabel("array size")
plt.ylabel("ratio python/fortran")
fig.tight_layout()
# plt.show()
# plt.bar(dims, pure_overhead)
plt.savefig("output.png", format="png")
