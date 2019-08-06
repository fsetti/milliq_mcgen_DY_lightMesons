import ROOT as r
import numpy as np
import sys
import os

particles = ["b_jpsi", "jpsi", "etaprime_omega", "etaprime_photon", "eta", "omega", "omega_pi0", "pi0", "phi", "rho", "b_psiprime", "psiprime"]
masses = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7]
charges = [0.01, 0.02, 0.05, 0.07, 0.1, 0.14, 0.2, 0.3]

for ptype in particles:
    for m in masses:
        for q in charges:
            print(ptype, m, q)
            dname = os.path.join("m_"+str(m).replace(".","p"), "q_"+str(q).replace(".","p"))            
            fname = os.path.join(dname, ptype+".root")
            if not os.path.isfile(fname):
                continue
            myFile = r.TFile(fname)
            print("opening..." + fname)
            output = open(os.path.join(dname,"{0}.txt".format(ptype)), "w")
            myTree = myFile.Get("Events")
            for i in myTree:
                if i.hit_p_xyz.Z() != 0:
                    output.write("{0} {1} {2} {3} {4} {5} {6} {7} {8}\n".format(i.sim_q, i.p4_m.M(), 
                                                                                i.hit_p_xyz.Z(), i.hit_p_xyz.X(), i.hit_p_xyz.Y(), 
                                                                                i.hit_p_p4.Pz(), i.hit_p_p4.Px(), i.hit_p_p4.Py(), 
                                                                                i.sim_q**2 * i.xsec * i.BR_q1 * i.filter_eff * 1000 / i.n_events_total))
                if i.hit_m_xyz.Z() != 0:
                    output.write("{0} {1} {2} {3} {4} {5} {6} {7} {8}\n".format(i.sim_q, i.p4_m.M(), 
                                                                                i.hit_m_xyz.Z(), i.hit_m_xyz.X(), i.hit_m_xyz.Y(), 
                                                                                i.hit_m_p4.Pz(), i.hit_m_p4.Px(), i.hit_m_p4.Py(), 
                                                                                i.sim_q**2 * i.xsec * i.BR_q1 * i.filter_eff * 1000 / i.n_events_total))


