import os
from textwrap import dedent

iseed = 0

def get_card_mq(
        model,
        ncores=1,
        nevents=10000,
        mgoutputname="./runs/out_test_v1/test_v1",
        carddir="./runs/out_test_v1/",
        kappa=1.0,
        mass=25.0,
        unique_seeds=True,
        ):
    global iseed
    seedstr = ""
    if unique_seeds:
        iseed += 1
        seedstr = "set run_card iseed {}".format(iseed)

    template = dedent("""
    set auto_update 0
    set run_mode 2
    set nb_core {ncores}

    {importstr}

    define p = p b b~
    define j = j b b~
    generate p p > {particle}+ {particle}-
    add process p p > {particle}+ {particle}- j

    output {mgoutputname} -nojpeg
    launch
    
    set param_card MASS {pid} {mass}
    {kappaparam}
    set run_card ebeam1 6500.0
    set run_card ebeam2 6500.0
    set run_card nevents {nevents}
    set run_card use_syst False

    set run_card ptl -1.0
    set run_card etal -1.0
    set run_card ickkw 0
    set run_card xqcut 0.0

    {seedstr}
    """)

    if model in ["mq5","mq"]:
        return template.format(
                ncores=ncores,
                nevents=nevents,
                mass = mass,
                mgoutputname=mgoutputname,
                importstr = "import model mq5_UFO-full",
                particle = "e",
                pid = 11,
                kappaparam = "set param_card TEMP 11 {kappa}".format(kappa=kappa),
                seedstr=seedstr,
                )
    if model == "mq4":
        return template.format(
                ncores=ncores,
                nevents=nevents,
                mass = mass,
                mgoutputname=mgoutputname,
                importstr = "import model_v4 mq4_UFO",
                particle = "mq",
                pid = 300015,
                kappaparam = "",
                seedstr=seedstr,
                )

def write_card(s,fname,dryrun=False):
    if dryrun:
        print("Would write {}".format(fname))
        return
    with open(fname,"w") as fh:
        fh.write(s)

# for model in ["mq4","mq5"]:
for model in ["mq5"]:
    carddir = "./runs/out_{model}_13tev_v1/".format(model=model)
    os.system("mkdir -p {}".format(carddir))
    kappa = 1.0
    nevents=10000
    njobs_per_mass = 3
    # for mass in [0.1,0.28,0.43,0.6,0.78,1.0,1.25,1.52,1.84,2.2,2.6,3.04,3.54,4.1,4.71,5.4,6.15,6.98,7.9,8.9,10.0,11.2,12.5,14.0,15.5,17.2,19.1,21.1,23.3,25.6,28.2,30.9,33.9,37.1,40.5,44.2,48.2,52.5,57.1,62.1,67.4,73.0,79.1,85.6,92.6,100.]:
    for mass in [0.1,0.28,0.43,0.6,0.78,1.0]:
        for chunk in range(njobs_per_mass):
            tag = "{model}_{mass}_{kappa}_chunk{chunk}".format(model=model,mass=str(mass).replace(".","p"),kappa=str(kappa).replace(".","p"),chunk=chunk)
            mgoutputname = "{carddir}/{tag}".format(carddir=carddir,tag=tag)
            cardname = "{carddir}/proc_card_{tag}.dat".format(carddir=carddir,tag=tag)
            buff = get_card_mq(model=model,ncores=1,mgoutputname=mgoutputname,carddir=carddir, mass=mass,kappa=kappa,nevents=nevents)
            write_card(buff,cardname,dryrun=False)


