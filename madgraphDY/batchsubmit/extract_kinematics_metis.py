import extract_kinematics as ek

fin = "./cards/mgoutput/Events/run_01/unweighted_events.lhe.gz"
fout = "./cards/mgoutput/Events/run_01/mcp_p4s.txt"

ek.simple_parse(fin, fout)


