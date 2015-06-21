
Name "pyliteco"
Outfile "pyliteco-setup.exe"

InstallDir "C:\Program Files (x86)\pyliteco"


RequestExecutionLevel admin


SilentInstall silent
SilentUninstall silent


!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
        messageBox mb_iconstop "Administrator rights required!"
        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        quit
${EndIf}
!macroend


!include LogicLib.nsh


Section "install"

	!insertmacro VerifyUserIsAdmin

	SetOutPath $INSTDIR

	writeUninstaller "$INSTDIR\uninstall.exe"

	# Do driver
	SetOutPath $INSTDIR\pylightco-driver
	File /r "pylightco-driver\"
	ExecWait "dpinst64.exe /sw"

	# And main service
	SetOutPath $INSTDIR
	StrCpy $0 "pyliteco-service.exe"
	File "/oname=$0" "dist\win_service.exe"
	SimpleSC::InstallService "pyliteco" "PyLiteCo" 16 2 "$INSTDIR\$0"
	SimpleSC::StartService "pyliteco" '' 15

	# Readme
	File "README.md"

SectionEnd

Section "uninstall"

	!insertmacro VerifyUserIsAdmin

	# Stop and remove service
	SimpleSC::StopService "pyliteco" '' 15
	SimpleSC::RemoveService "pyliteco"

	# remove files
	rmDir /r "$INSTDIR\pylightco-driver\"
	delete "$INSTDIR\pyliteco.json"
	delete "$INSTDIR\pyliteco-service.exe"
	delete "$INSTDIR\README.md"

	delete "$INSTDIR\uninstall.exe"

	rmDir $INSTDIR

SectionEnd