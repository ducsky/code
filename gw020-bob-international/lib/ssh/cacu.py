def Convert_SSID(a = '', b = ''):
	u = int(a,16)
	k = int(b, 16)
	return (u-k)
def Insert_BSSID(a = ''):
	u = int(a,16)
	k = u-1
	return hex(k)
print Insert_BSSID(a = 'A77') 

