import json
import numpy as np
import matplotlib.pyplot as plt

d = json.load(open("systs/v8_v1_save2m.json"))

vals = {}
for sq in d:
    q = float(sq.split("_")[1].replace("p","."))
    for sm in d[sq]:
        m = float(sm.split("_")[1].replace("p","."))
        if m not in vals:
            vals[m] = []
        s = 0
        if "material" in d[sq][sm]:
            s = d[sq][sm]["material"][0]
        vals[m].append((q,s))

plt.figure()

mtoplot = [0.05, 0.1, 0.5, 1.0, 2.0]
for m in mtoplot:
    sl = sorted(vals[m])
    qs = [x[0] for x in sl]
    ss = [x[1] for x in sl]
    plt.plot(qs, ss, 'o-', label="m = "+str(m))
plt.gca().set_xscale("log")
plt.legend(loc="upper left")
plt.xlabel("Q/e")
plt.ylabel("material variation systematic")

plt.savefig("/home/users/bemarsh/public_html/milliqan/material_systematic.pdf")

# plt.show()
