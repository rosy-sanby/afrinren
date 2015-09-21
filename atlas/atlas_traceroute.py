#!/usr/bin/python
import sys
import traceback
import os
import time
import socket
import measure_baseclass
from measure_baseclass import MeasurementBase
from measure_baseclass import load_input, readkey, process_response
from measure_baseclass import SLEEP_TIME

class Traceroute(MeasurementBase):

    def __init__(self, target, key, probe_list=None, sess=None, 
                dont_frag=False, protocol='ICMP', timeout=4000, paris=0, start_time=None, stop_time=None):
        super(Traceroute, self).__init__(target, key, probe_list, sess, start_time, stop_time)
        self.measurement_type = 'traceroute'
       
        self.dont_frag = dont_frag
        self.protocol = protocol
        self.timeout = timeout
        self.paris = paris
        
    def setup_definitions(self):
    
        definitions = super(Traceroute, self).setup_definitions()
        
        definitions['dontfrag'] = str(self.dont_frag).lower()
        definitions['protocol'] = self.protocol 
        definitions['timeout'] = self.timeout
        
        if self.paris >= 1 and self.paris <= 16:
            definitions['paris'] = self.paris        

        return definitions

def config_argparser():

    parser = measure_baseclass.config_argparser()
    parser.add_argument('-p', '--protocol', default=['ICMP'], nargs=1, help='Must be ICMP or UDP (default: ICMP)')
    parser.add_argument('--dont-frag', action='store_true', help='Don\'t fragment the packet (default: off)')
    parser.add_argument('--paris', default=[0], 
                        help='Use Paris. Value must be between 1 and 16. (default: off)')
    parser.add_argument('--timeout', default=[4000], type=int, # list default and type=int do not seem to work
                        help='Value (in milliseconds) must be between 1 and 60000 (default: 4000)')
    parser.add_argument('--npackets', default=[3], nargs=1,
                        help='Number of packets to send to each hop (default: 3)')
    return parser

if __name__ == '__main__':
    
    parser = config_argparser()  #set up command line parameters
    args = parser.parse_args()

    try:
        key_file = args.key_file[0]
        key = readkey(key_file)          #read in Atlas API key
    except:
        sys.stderr.write('Error reading key file at %s\n' % key_file)
        sys.exit(1)

    #get args
    target_dict = load_input(args.target_list[0])
    outfile = args.meas_id_output[0]
    dont_frag = args.dont_frag
    protocol = args.protocol[0]
    timeout = args.timeout[0]
    paris = args.paris[0]
    is_public = args.private
    ipv6 = args.ipv6
    description = args.description[0]
    repeating = args.repeats[0]
    npackets = args.npackets[0]
    start_time=args.start_time[0]
    stop_time=args.stop_time[0]

    if not target_dict:
        sys.stderr.write('No targets defined\n')
        sys.exit(1)

    try:
        outf = open(outfile, 'w')

        i = 0
        target_list = target_dict.keys()
        #print(target_list)
        while i < len(target_list):
           
            try: 
                target = target_list[i]
                probe_list = target_dict[target]
                #print(probe_list)
                """
                The maxmimum number of probes per request is 500 so we need to break
                this is up into several requests.
                """
                probe_list_chunks = [probe_list[x:x+500] for x in xrange(0, len(probe_list), 500)]
                j = 0
                #for probe_list_chunk in probe_list_chunks:
                while j < len(probe_list_chunks):

                    probe_list_chunk = probe_list_chunks[j]
                    
                    traceroute = Traceroute(target, key, probe_list=probe_list_chunk, 
                                            dont_frag=dont_frag, protocol=protocol, timeout=timeout, paris=paris, 
                                            start_time=start_time, stop_time=stop_time)
                    traceroute.description = description
                    traceroute.af = 4 if not ipv6 else 6
                    traceroute.is_oneoff = True if repeating == 0 else False
                    if not traceroute.is_oneoff: traceroute.interval = repeating #set the repeating interval
                    traceroute.is_public = True if not is_public else False
                    traceroute.npackets = npackets

                    response = traceroute.run()
                    status, result = process_response(response)

                    if status == 'error':
                        sys.stderr.write('Request got error %s. Sleeping for %d seconds\n' % (result, SLEEP_TIME))
                        time.sleep(SLEEP_TIME)
                        continue #try again
                    else:  #on success
                        measurement_list = result
                        measurement_list_str = map(str, measurement_list)
                        outstr = '\n'.join(measurement_list_str)
                        outf.write(outstr+'\n')
                        print(outstr)
                        j += 1 #only increment on success
                        time.sleep(10)
                    
                i += 1
            except socket.error:
                sys.stderr.write('Got network error. Going to sleep for %d seconds\n' % SLEEP_TIME)
                traceback.print_exc(file=sys.stderr)
                time.sleep(SLEEP_TIME)
    except:
        sys.stderr.write('Got error making traceroute request\n')
        traceback.print_exc(file=sys.stderr)
    finally:
        outf.close()
