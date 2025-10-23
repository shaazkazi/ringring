[Setup]
AppName=Ring Ring
AppVersion=1.0
AppPublisher=ShaazKazi
AppPublisherURL=https://github.com/ShaazKazi/ringring
AppSupportURL=https://github.com/ShaazKazi/ringring
AppUpdatesURL=https://github.com/ShaazKazi/ringring
DefaultDirName={autopf}\Ring Ring
DefaultGroupName=Ring Ring
AllowNoIcons=yes
LicenseFile=
OutputDir=installer_output
OutputBaseFilename=Ring_Ring_Setup
SetupIconFile=assets\logo\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\RingRing.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Ring Ring"; Filename: "{app}\RingRing.exe"; IconFilename: "{app}\assets\logo\app_icon.ico"
Name: "{group}\{cm:UninstallProgram,Ring Ring}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Ring Ring"; Filename: "{app}\RingRing.exe"; IconFilename: "{app}\assets\logo\app_icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Ring Ring"; Filename: "{app}\RingRing.exe"; IconFilename: "{app}\assets\logo\app_icon.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\RingRing.exe"; Description: "{cm:LaunchProgram,Ring Ring}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Ring Ring"; ValueData: "{app}\RingRing.exe"; Flags: uninsdeletevalue; Tasks: startupicon

[Tasks]
Name: "startupicon"; Description: "Start Ring Ring automatically when Windows starts"; GroupDescription: "Startup Options";