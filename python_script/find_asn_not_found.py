import sys
import subprocess

ips = open(sys.argv[1], 'r')
lines = ips.readlines()
ips.close()

count=0
edited_ips = open(sys.argv[1]+"edited",'w')
for line in lines:
    count+=1
  
    info = line.split(", ")
    if len(info)<3:
        print(str(count)+" out of "+str(len(lines)))
        myfile=open("whois.txt",'w')
        subprocess.call(['whois', '-h', 'whois.arin.net', info[0]],stdout=myfile)
        myfile.close()
        try:
            grep = subprocess.check_output(['grep', 'OriginAS:', 'whois.txt'])
        except:
            grep="OriginAS: Unknown"
        if grep.split(":")[1].strip()=="OriginAS":
            edited_ips.write(info[0]+", "+grep.split(":")[2].strip())
        else:
            edited_ips.write(info[0]+", "+grep.split(":")[1].strip()+'\n')
    else:
        edited_ips.write(line)
edited_ips.close()
