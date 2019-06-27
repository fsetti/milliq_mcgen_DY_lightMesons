## milliq_mcgen

A collection of tools for generating signal Monte Carlo for the Milliqan experiment:
* Compute cross sections and branching ratios for all main m<sub>CP</sub> decay modes
* Simulate both two-body and Dalitz decays of parent particles into m<sub>CP</sub>'s
* Generate root files with all relevant information needed to feed generated m<sub>CP</sub>'s into propagation/simulation software

<p align="center">
<img src="./scripts/plot_xsecs/mcp_xsec.png" alt="plot of mCP cross sections" width="700"/>
</p>

### Contents of subdirectories:

`decayMCP`: Main program to generate mCP decays

`docs`: Documentation

`oniaDirect`: Various tools/data for direct onia production

`oniaFromB`: Theoretical distributions of onia from b decays

`mesonPt`: pT distributions for direct production of non-onia mesons (pi, rho, omega, phi, eta)

`scripts`: scripts to calculate Dalitz and Onia BR, perform two-body and Dalitz decays, and plot/extract mCP cross sections

`utils`: helper C++ functions to compute branching ratios and decay kinematics
