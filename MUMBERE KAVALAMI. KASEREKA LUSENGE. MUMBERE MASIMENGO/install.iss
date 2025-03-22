[Setup]
AppName=Cryptographie
AppVersion=1.0
AppVerName=CryptoAnalyse 1.0
DefaultDirName={pf}\Cryptographie
DefaultGroupName=Cryptographie
OutputDir=.
OutputBaseFilename=Cryptographie_Installer
Compression=none

[Files]
Source: "dist\Cryptographie.exe"; DestDir: "{app}"; Flags: ignoreversion




[Icons]
Name: "{group}\Cryptographie"; Filename: "{app}\Cryptographie.exe"
Name: "{userdesktop}\Cryptographie"; Filename: "{app}\Cryptographie.exe"

