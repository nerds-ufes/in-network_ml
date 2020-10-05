#!/usr/bin/env python
# python histograma.py -f test/*.bwm -o host > histograma.txt

import matplotlib as m
m.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import argparse
import collections

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Rate timeseries output to one plot",
                    required=True,
                    action="store",
                    nargs='+',
                    dest="files")

parser.add_argument('--type', '-t',
                    help="Operation desired",
                    required=True,
                    action="store",
                    dest="type")

parser.add_argument('--out', '-o',
                    help="Operation desired",
                    required=True,
                    action="store",
                    dest="output")

args = parser.parse_args()

def read_list(fname, delim=','):
    lines = open(fname).xreadlines()
    ret = []
    for l in lines:
        ls = l.strip().split(delim)
        ls = map(lambda e: '0' if e.strip() == '' or e.strip() == 'ms' or e.strip() == 's' else e, ls)
        ret.append(ls)
    return ret

# Somar trafego total
if args.type == "total":
	for f in args.files:
		data = read_list(f)
		total=0
		time=0
		time_end=0
		column = 3 # column with RX bytes
		for row in data:
			try:
				if "total" in row:
					time += 1
					nbytes = float(row[column])
					total = total + nbytes
					if nbytes < 1000 and time_end == 0 and time > 10:
						time_end=time
			except:
				break
		print "Topology, Mbytes"
		print "%s,%d,%d" % (f.strip().split('/')[1], total * 8.0 / (1 << 20), time_end)

# Somar trafego por interface
if args.type == "interface":
	for f in args.files:
		data = read_list(f)
		histogram_data = dict()
		c_key  = 1 # column with interfaces
		c_data = 3 # column with RX bytes
		for row in data:
			try:
				if row[c_key] not in ["eth0", "lo", "total"]:
					nbytes = float(row[c_data])
					if row[c_key] not in histogram_data:
						histogram_data[row[c_key]] = 0
					histogram_data[row[c_key]] += nbytes
					#if row[c_key] == "10_1_1-eth1":
					#	print "%s --> %d" % (row[c_key], histogram_data[row[c_key]])			
			except:
				break
				
		print "Topology, Interface, Mbytes"
		for key, value in histogram_data.iteritems():
			print "%s,%s,%d" % (f.strip().split('/')[1], key, histogram_data[key] * 8.0 / (1 << 20))


# Somar trafego por host
if args.type == "host":
	for f in args.files:
		data = read_list(f)
		histogram_data = dict()
		c_key  = 1 # column with interfaces
		c_data = 3 # column with RX bytes
		for row in data:
			try:			
				if row[c_key] not in ["eth0", "lo", "total"]:
					key = row[c_key].split('-')[0]
					nbytes = float(row[c_data])
					if key not in histogram_data:
						histogram_data[key] = 0
					histogram_data[key] += nbytes
			except:
				break
		print "Topology, Host, Mbytes"
		values = []
		keys = []
		od = collections.OrderedDict(sorted(histogram_data.items())) # ordena os dados pelas chaves
		for key, value in od.iteritems():
			print "%s,%s,%d" % (f.strip().split('/')[1], key, value * 8.0 / (1 << 20)) # converte para Mbps
			values.append(value * 8.0 / (1 << 20))
			keys.append(key)
			
		loc_values = np.arange(len(values))
		loc_keys = np.arange(len(keys))
		figure = plt.figure()
		width = 0.5
		plt.bar(loc_values+0.5, values, width, color='g')
		plt.title("Histogram")
		plt.ylabel("Mbps")
		plt.xticks(loc_keys+0.8, keys, rotation=90)		
		plt.xlabel("Hosts")
		plt.gcf().subplots_adjust(bottom=0.18, left=0.1, right=0.97, top=0.93)
		plt.grid(True)
		figure.savefig(args.output, format="png", dpi = 200)
		plt.show()


