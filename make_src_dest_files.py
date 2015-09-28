#my_probes.txt ../address_african

ips_file = open("data/address_african", 'r')

ips = ips_file.readlines()
count = 1
for ip in ips:
    new_filename = "measurements/target_and_probes_"+str(count)+".txt"
    count+=1
    probes_file = open("data/my_probes.txt", 'r')
    probes = probes_file.readlines()
    probes_file.close()
    new_file = open(new_filename, 'w')
    for probe in probes:
        new_file.write(ip.strip() + " " +probe.split()[0]+"\n")
    new_file.close()
    
ips_file.close()
