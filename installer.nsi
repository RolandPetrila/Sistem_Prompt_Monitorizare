; NSIS Installer Script for AI Prompt Generator Ultimate
; Requires NSIS 3.x

!define APP_NAME "AI Prompt Generator Ultimate"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "AI Tools"
!define APP_EXEC "AIPromptGenerator.exe"
!define APP_DIR "AIPromptGenerator"

!include "MUI2.nsh"

; Installer Information
Name "${APP_NAME}"
OutFile "AIPromptGenerator_Setup_${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES64\${APP_DIR}"
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installation
Section "Application" SecMain
    SectionIn RO
    
    ; Set output path
    SetOutPath "$INSTDIR"
    
    ; Install files
    File "dist\${APP_EXEC}"
    File "README.md"
    File "LICENSE"
    
    ; Create directories
    CreateDirectory "$INSTDIR\config"
    CreateDirectory "$INSTDIR\backups"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Registry entries
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_DIR}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_DIR}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_DIR}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_DIR}" "UninstallString" "$INSTDIR\Uninstall.exe"
    
    ; Start menu shortcut
    CreateDirectory "$SMPROGRAMS\${APP_DIR}"
    CreateShortcut "$SMPROGRAMS\${APP_DIR}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXEC}"
    CreateShortcut "$SMPROGRAMS\${APP_DIR}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    
    ; Desktop shortcut
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXEC}"
SectionEnd

Section "Start Menu Shortcut" SecShortcut
    ; Already created above
SectionEnd

; Uninstaller
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\${APP_EXEC}"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove directories (keep user data)
    RMDir /r "$INSTDIR\config"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\${APP_DIR}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_DIR}\Uninstall.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\${APP_DIR}"
    
    ; Remove registry
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_DIR}"
    
    ; Remove installation directory
    RMDir "$INSTDIR"
SectionEnd

