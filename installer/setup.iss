; VietDub Inno Setup Script
; Creates professional Windows installer

#define MyAppName "VietDub"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "VietDub Team"
#define MyAppURL "https://github.com/yourusername/visub"
#define MyAppExeName "VietDub.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Output settings
OutputDir=output
OutputBaseFilename=Visub_Setup
; Compression for smaller file
Compression=lzma2/ultra64
SolidCompression=yes
; Require admin for Program Files
PrivilegesRequired=admin
; Modern Windows versions
MinVersion=10.0
; Wizard style
WizardStyle=modern
WizardSizePercent=120
; Icon (optional - remove if no icon)
; SetupIconFile=..\assets\icon.ico
; Uninstaller
UninstallDisplayIcon={app}\{#MyAppExeName}
; License (optional)
; LicenseFile=..\LICENSE

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Copy all files from PyInstaller dist folder
Source: "..\dist\VietDub\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; FFmpeg binary (if bundled separately)
; Source: "..\ffmpeg\*"; DestDir: "{app}\ffmpeg"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Option to run app after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Custom code to show welcome message
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel2.Caption := 
    'VietDub - AI Video Dubbing Tool' + #13#10 + #13#10 +
    'This will install VietDub on your computer.' + #13#10 + #13#10 +
    'Features:' + #13#10 +
    '• AI-powered transcription (Whisper)' + #13#10 +
    '• Automatic translation to Vietnamese' + #13#10 +
    '• Text-to-Speech dubbing' + #13#10 +
    '• Video export with subtitles' + #13#10 + #13#10 +
    'Click Next to continue.';
end;
