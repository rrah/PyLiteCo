Outfile "pyliteco-setup.exe"

InstallDir "C:\Program Files (x86)\pyliteco"

Section

	SetOutPath $INSTDIR

	# Check user is admin
	UserInfo::getAccountType
	Pop $0
	StrCmp $0 "Admin" +2
	Return

	# Do driver
	SetOutPath $INSTDIR\pylightco-driver
	File /r "pylightco-driver\"
	ExecWait "dpinst64.exe"

	# And main service
	SetOutPath $INSTDIR
	File "pyliteco-service.exe"
	ExecWait "pyliteco-service.exe install"
	ExecWait "pyliteco-service.exe start"

SectionEnd