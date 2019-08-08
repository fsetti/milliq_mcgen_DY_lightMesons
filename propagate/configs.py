
class Config:
    def __init__(self, name):
        self.det_width = 1.0
        self.det_height = 1.0
        self.dt = 0.1

        if name == "MQ":
            self.mat_setup = 'cms'
            self.bfield = 'cms'            
            self.dist_to_detector = 33.
            self.eta = 0.11
            self.rock_begins = self.dist_to_detector - 17.
            self.max_nsteps = 3800
            self.etamin = self.eta - 0.18
            self.etamax = self.eta + 0.18
            self.phimin = -0.03
            self.phimax = 2.4
            self.m_vals = [0.01, 0.05, 0.1,  0.2, 0.3, 0.4, 0.5, 0.7, 1.0, 1.4, 1.6, 1.8, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]
            self.pt_cuts = [0.10, 0.15, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.2, 1.4, 1.8, 2.2, 2.5, 3.0, 3.5]

        elif name == "mapp_theta25":
            self.mat_setup = 'justrock'
            self.bfield = 'none'
            self.dist_to_detector = 33.
            self.eta = 1.51
            self.rock_begins = self.dist_to_detector - 26.
            self.max_nsteps = 3800
            self.etamin = self.eta - 0.10
            self.etamax = self.eta + 0.10
            self.phimin = -0.05
            self.phimax = 0.05
            self.m_vals = None
            self.pt_cuts = None

        elif name == "mapp_theta10":
            self.mat_setup = 'justrock'
            self.bfield = 'none'
            self.dist_to_detector = 45.
            self.eta = 2.44
            self.rock_begins = self.dist_to_detector - 32.
            self.max_nsteps = 5200
            self.etamin = self.eta - 0.20
            self.etamax = self.eta + 0.20
            self.phimin = -0.10
            self.phimax = 0.10
            self.m_vals = None
            self.pt_cuts = None

        elif name == "mapp_theta5":
            self.mat_setup = 'justrock'
            self.bfield = 'none'
            self.dist_to_detector = 55.
            self.eta = 3.13
            self.rock_begins = self.dist_to_detector - 10.
            self.max_nsteps = 6400
            self.etamin = self.eta - 0.30
            self.etamax = self.eta + 0.30
            self.phimin = -0.20
            self.phimax = 0.20
            self.m_vals = None
            self.pt_cuts = None

        else:
            raise Exception("Unknown config name "+name)
