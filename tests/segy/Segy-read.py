import matplotlib.pyplot as plt
import segyio
import pandas as pd

segyfile = 'sample1.SGY'

f = segyio.open(segyfile, ignore_geometry=True)

clip = 1e+2
vmin, vmax = -clip, clip

# Figure
figsize=(20, 20)
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=figsize, facecolor='w', edgecolor='k',
                       squeeze=False,
                       sharex=True)
axs = axs.ravel()
im = axs[0].imshow(f.trace.raw[:].T, cmap=plt.cm.seismic, vmin=vmin, vmax=vmax)

print(pd.DataFrame(f))
plt.show()