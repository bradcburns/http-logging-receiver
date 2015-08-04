import ConfigParser
from sys import argv
from bottle import route, run, request, response, post
from time import localtime, strftime

@post('/log')
def ReceivePostLog():

	strLogLine = FormatLogLine(request.forms, request.remote_addr)

	if WriteLogLine(strLogLine):
		response.status = 200
		return 'log accepted.'
	else:
		response.status = 500
		return 'something went wrong.'

def FormatLogLine(RawQueryData,RequestIPAddr):
	strTimestamp = UnixToLocalTimeString(localtime(float(RawQueryData['created'])))
	strLoggerName = RawQueryData['name']
	strIP = RequestIPAddr
	strMsg = RawQueryData['msg']
	strFile = RawQueryData['filename']
	strSeverity = RawQueryData['levelname']


	if not (RawQueryData['exc_info']) == 'None':
		strExceptionData = RawQueryData['exc_info'] + ' at line ' + RawQueryData['lineno']
	else:
		strExceptionData = 'at line ' + RawQueryData['lineno']

	listLogLine = ([strSeverity,
		strTimestamp,
		strIP,
		strFile,
		strMsg,
		strExceptionData])

	strLogLine = ' > '.join(listLogLine)

	return strLogLine

def UnixToLocalTimeString(UnixTimeInDecimal):
	ret = strftime('%a %x %H:%M:%S',UnixTimeInDecimal)
	return ret

def WriteLogLine(strFilename,strLogLine):
	with open(strProcess + '.log','w') as f:
		f.write(strLogLine)

	return True

def GetConfig(pathConfigFile):
	parser = ConfigParser.ConfigParser()
	parser.read(pathConfigFile)

	retDict = ({
		'hostname':parser.get('NETWORK','IPAddress'),
		'port':parser.getint('NETWORK','Port')
		})

	return retDict

if __name__ == '__main__':
	config = GetConfig(argv[1])
	run(hostname=config['hostname'],port=config['port'])

