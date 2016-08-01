import os
import stat

score = 0
totalScore = 44

#tomcat klasoru /opt/tomcat/ olacak sekilde yazildi

tomcatDir = 'tomcat'
testResult = open("test.txt", "w+")

#Gereksiz dosya testi

junk_files = ['webapps/docs', 'webapps/examples', 'webapps/ROOT/RELEASE-NOTES.txt', 'webapps/host-manager', 'work/Catalina/localhost/docs', 'work/Catalina/localhost/examples', 'work/Catalina/localhost/host-manager', 'work/Catalina/localhost/manager' ]

for f in junk_files:
	
	file_path = '/opt/' + tomcatDir + '/' + f
	#fp = os.popen('sudo grep "[[:space:]]/opt[[:space:]]" ' + file_path)
	#result = fp.read()

	if(os.path.isfile(file_path) or os.path.isdir(file_path)):
		testResult.write('Dosya ' + file_path + ' silinmemis\n')
	else:
		testResult.write('Dosya ' + file_path + ' silinmis\n')
		score+=1

#check tomcat directory file permissons testi

for f in os.listdir('/opt/' + tomcatDir):
	st = os.stat('/opt/' + tomcatDir + '/' + f)
	file_name = os.path.basename(f)
	if(bool(st.st_mode and stat.S_ISDIR)):
		testResult.write('Kullanicinin ' + file_name  + ' dosyasi icin rw  yetkisi var\n')		
	else:
		testResult.write('Kullanicinin ' + file_name  + ' dosyasi icin rw yetkisi yok\n')	
		score+=1
#Server xml testi

serverXML = open('/opt/' + tomcatDir + '/conf/server.xml', 'r').read()

if('xpoweredBy="false"' in serverXML and 'allowTrace="false"' in serverXML):
	testResult.write('Allow trace ve xpoweredBy kapali\n')	
	score+=5
else:
	testResult.write('Allow trace ve xpoweredBy acik\n')

if('<Server port="-1" shutdown="SHUTDOWN">'in serverXML):
	testResult.write('Port = -1\n')	
	score+=5
else:
	testResult.write('Port = 8005 \n')	
if('autoDeploy="false"'in serverXML):
	testResult.write('Auto deploy kapali\n')	
	score+=5
else:
	testResult.write('Auto deploy acik\n')	

#SSL testi

if('keystorePass'in serverXML and 'keyAlias' in serverXML):
	testResult.write('SSL kapali\n')	
	score+=5
else:
	testResult.write('SSL kapali\n')

#http only testi
contextXML = open('/opt/'+ tomcatDir +'/conf/context.xml', 'r').read()

if('usehttponly="true"'in contextXML):
	testResult.write('usehttponly acik\n')	
	score+=5
else:
	testResult.write('usehttponly kapali\n')


testResult.write('Skor: ' +  str(score) + '/' + str(totalScore))
testResult.close()
