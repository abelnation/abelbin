
import re

HOSTS_FILE = '/etc/hosts'
WORKTIME_SITES_FILE = './disabledsites.txt'

DISABLED_HOSTNAME = '127.0.0.1'

def main():
	IS_WORKTIME = False

	infile = open(HOSTS_FILE, 'r')
	host_lines = infile.readlines()
	infile.close()

	worktime_sites = open(WORKTIME_SITES_FILE).readlines()

	outfile = open(HOSTS_FILE, 'w')

	for line in host_lines:
		print line

		worktime_regex = "IS_WORKTIME = (True|False)"
		worktime_match = re.search(worktime_regex, line)
		if worktime_match != None:
			if worktime_match.group(1) == "True":
				IS_WORKTIME = True
			else:
				IS_WORKTIME = False
			print "IS_WORKTIME: %s" % IS_WORKTIME
			outfile.write("# IS_WORKTIME = %s\n" % ("False" if IS_WORKTIME else "True"))
			continue


		is_disabled_site = False
		disabled_hostname = ""

		for hostname in worktime_sites:
			if is_disabled_site:
				continue

			hostname = hostname.strip()

			host_regex = "\s%s\s" % (hostname)
			if re.search(host_regex, line) != None:
				is_disabled_site = True
				disabled_hostname = hostname

		if is_disabled_site:
			outfile.write("%s%s\t%s\n" % (("# " if IS_WORKTIME else ""), DISABLED_HOSTNAME, disabled_hostname))
		else:
			outfile.write(line)

	outfile.close()

if __name__ == '__main__':
	main()