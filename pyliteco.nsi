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
	StrCpy $0 "pyliteco-service.exe"
	File "pyliteco-service.exe"
	SimpleSC::InstallService "pyliteco" "PyLiteCo" 16 2 "$INSTDIR\$0"
	SimpleSC::StartService "pyliteco" '' 15

SectionEnd