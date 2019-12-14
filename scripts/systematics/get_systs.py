import os
import json

TAG = "v8_v1_save2m"

rates = json.load(open(os.path.join("rates", TAG+".json")))
rates_dens = json.load(open(os.path.join("rates", TAG+"_dens1p07"+".json")))
systs = {}

for sq in rates:
    systs[sq] = {}
    for sm in rates[sq]:
        systs[sq][sm] = {}
        d = rates[sq][sm]
        rate = "line_rate"
        tot = d["total"]["line_rate_cn"]
        if tot==0:
            rate = "rate"
            tot = d["total"]["rate_cn"]
        systs[sq][sm]["minbias_xs"] = [0.0, 0.0]
        for p in d:
            if p=="total":
                continue
            sp = p
            if "omega" in p:
                sp = "omega"
            if "etaprime" in p:
                sp = "etaprime"
            if sp+"_xs" not in systs[sq][sm]:
                systs[sq][sm][sp+"_xs"] = [0.0, 0.0]
            cn = d[p][rate+"_cn"]
            if "psi" not in sp and "ups" not in sp:
                systs[sq][sm][sp+"_xs"][0] += 0.30 * cn
                systs[sq][sm][sp+"_xs"][1] -= 0.30 * cn
                if "dy" not in sp:
                    systs[sq][sm]["minbias_xs"][0] += 10./80. * cn
                    systs[sq][sm]["minbias_xs"][1] -= 10./80. * cn
            else:
                systs[sq][sm][sp+"_xs"][0] += d[p][rate+"_up"] - cn
                systs[sq][sm][sp+"_xs"][1] += d[p][rate+"_dn"] - cn

        nom_rate = d["total"]["rate_cn"]
        dens_rate = rates_dens[sq][sm]["total"]["rate_cn"]
        s = abs(nom_rate-dens_rate) * tot/nom_rate
        systs[sq][sm]["material"] = [s, -s]

        for s in systs[sq][sm].keys():
            if tot==0:
                print sq, sm, s
            systs[sq][sm][s][0] /= tot
            systs[sq][sm][s][1] /= tot
            if systs[sq][sm][s][0] < 0.001 and systs[sq][sm][s][1] < 0.001:
                del systs[sq][sm][s]

json.dump(systs, open(os.path.join("systs", TAG+".json"), 'w'), ensure_ascii=True, sort_keys=True, indent=4)



