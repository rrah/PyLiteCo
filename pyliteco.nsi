/*
Create Windows service installer for pyliteco

Author: Robert Walker <rrah99@gmail.com>

Copyright (C) 2015 Robert Walker
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; version 2.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/

Name "pyliteco"
Outfile "pyliteco-setup.exe"

InstallDir "$PROGRAMFILES\pyliteco"


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
!include locate.nsh


Section "install"

	!insertmacro VerifyUserIsAdmin

	SetOutPath $INSTDIR

	writeUninstaller "$INSTDIR\uninstall.exe"

	# And main service
	SetOutPath $INSTDIR
	StrCpy $0 "pyliteco-service.exe"
	File "/oname=$0" "dist\win_service.exe"
	Execwait '"$INSTDIR\pyliteco-service.exe" install'
	SimpleSC::StartService "pyliteco" '' 15
	
	# Readme
	File "README.md"
	
	${locate::GetSize} "$INSTDIR" "/S=Kb" $0 $1 $2
	IntFmt $0 "0x%08X" $0
	
	# Registry for uninstaller
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyliteco" \
					"DisplayName" "PyLiteCo"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyliteco" \
					"UninstallString" "$\"$INSTDIR\uninstall.exe$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyliteco" \
					"InstallLocation" "$\"$INSTDIR$\""
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyliteco" \
					"NoModify" "1"
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyliteco" \
					"NoRepair" "1"
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyliteco" \
					"EstimatedSize" "$0"

SectionEnd

Section "uninstall"

	!insertmacro VerifyUserIsAdmin

	# Stop and remove service
	SimpleSC::StopService "pyliteco" '' 15
	Execwait '"$INSTDIR\pyliteco-service.exe" remove'

	# remove files
	delete "$INSTDIR\pyliteco.json"
	delete "$INSTDIR\pyliteco-service.exe"
	delete "$INSTDIR\README.md"
	delete "$INSTDIR\pyliteco.log"

	# Remove registry entries
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyliteco"

	delete "$INSTDIR\uninstall.exe"

	rmDir $INSTDIR

SectionEnd