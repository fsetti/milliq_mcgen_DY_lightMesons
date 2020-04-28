import os,sys
import write_cards as wc

mass = float(sys.argv[1])
nevents = int(sys.argv[2])
chunk = int(sys.argv[3])

model = "mq5"
kappa = 1.0
carddir = "./cards"

os.system("mkdir -p "+carddir)

mgoutputname = "{0}/mgoutput".format(carddir)
cardname = "{0}/proc.dat".format(carddir)

wc.iseed = int(mass*1000) + chunk
buff = wc.get_card_mq(model=model, ncores=1, mgoutputname=mgoutputname, carddir=carddir,
                   mass=mass, kappa=kappa, nevents=nevents)
wc.write_card(buff, cardname, dryrun=False)
