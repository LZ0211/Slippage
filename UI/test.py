import numpy as np
from scipy.signal import find_peaks, find_peaks_cwt

data = np.array([-0.0233964671,
-0.0238269853,
-0.0244959337,
-0.0248558122,
-0.0241723333,
-0.0223032344,
-0.0198175048,
-0.0171829936,
-0.0153619246,
-0.0142289343,
-0.0129633293,
-0.0120749254,
-0.0114077755,
-0.0107137734,
-0.0102173705,
-0.0098824039,
-0.0094535592,
-0.0090208126,
-0.0089942331,
-0.009061368,
-0.0092184797,
-0.009658935,
-0.00985123,
-0.009646005,
-0.0099954581,
-0.010987131,
-0.01180556,
-0.0140836185,
-0.0136200364,
-0.0111110757,
-0.0091876135,
-0.0099730639,
-0.0214885868,
-0.0398080449,
-0.0713604089,
-0.1227067925,
-0.1535280579,
-0.1840126044,
-0.2281090447,
-0.2915448852,
-0.3805711737,
-0.4700645228,
-0.5604692094])

res = find_peaks(data,height=-0.2,threshold=0.0001)
print(res)