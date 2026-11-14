; SPDX-License-Identifier: GPL-2.0-or-later
Unicode true
!include "MUI2.nsh"
!include "x64.nsh"
!include "FileFunc.nsh"

Name "PandaKB Vial"
OutFile "${PACKAGE}"
InstallDir "$LOCALAPPDATA\PandaKB\Vial"
RequestExecutionLevel user
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "PandaKB Vial"
VIAddVersionKey "FileDescription" "PandaKB Vial Installer"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "LegalCopyright" "Vial contributors and PandaKB"
!define UNINSTALL_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\PandaKBVial"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\..\COPYING"
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\Vial.exe"
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Function .onInit
  ${IfNot} ${RunningX64}
    MessageBox MB_ICONSTOP "PandaKB Vial requires 64-bit Windows."
    SetErrorLevel 1
    Quit
  ${EndIf}
FunctionEnd

Section "PandaKB Vial"
  SetShellVarContext current
  SetOutPath "$INSTDIR"
  File /r "${BUNDLE}\*"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateShortcut "$SMPROGRAMS\PandaKB Vial.lnk" "$INSTDIR\Vial.exe"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayName" "PandaKB Vial"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "Publisher" "PandaKB"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayIcon" "$INSTDIR\Vial.exe"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "${UNINSTALL_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  SetShellVarContext current
  Delete "$SMPROGRAMS\PandaKB Vial.lnk"
  DeleteRegKey HKCU "${UNINSTALL_KEY}"
  !include "${REMOVE_LIST}"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
SectionEnd
