#my_probes.txt ../address_african

ips_file = open("data/address_african", 'r')
ips = ips_file.readlines()
ips_file.close()

probes_file = open("data/my_probes.txt", 'r')
probes = probes_file.readlines()
probes_file.close()

for ip in ips:
    for probe in probes:
        new_filename = "full_measurements/target_"+ip.strip()+"_and_probe_"+str(probe.split()[0])+".txt"
        new_file = open(new_filename, 'w')
        new_file.write(ip.strip() + " " +probe.split()[0])
        new_file.close()
