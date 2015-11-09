from numpy import sqrt, pi, exp, random
from lmfit import  Model

import matplotlib.pyplot as plt

x = range(20)
y = [n**2/sqrt((100-n**2)**2+(n/0.9)**2) for n in range(20)]

def resonance_lorentz(freq, resfreq, amp, guete):
    return amp * resfreq**2 / (
        guete * sqrt((freq**2 - resfreq**2)**2 + (freq * resfreq / guete)**2)
    )

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))

gmod = Model(resonance_lorentz)
result = gmod.fit(y, freq=x, resfreq=5, amp=5, guete=1)

print(result.fit_report())

plt.plot(x, y,         'bo')
plt.plot(x, result.init_fit, 'k--')
plt.plot(x, result.best_fit, 'r-')
plt.show()
