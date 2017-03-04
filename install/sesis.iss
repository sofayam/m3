; sesis.iss
; todo: add printing support to M3_PATH

[Setup]
AppName=Sesis Tools
AppVerName=Sesis Tools version 0.1
DefaultDirName={pf}\Sesis
DefaultGroupName=Sesis Tools
PrivilegesRequired=admin

[Files]
Source: "..\ChangeLog.txt"; DestDir: "{app}\m3"
Source: "..\bin\*"; DestDir: "{app}\m3\bin"; Flags: recursesubdirs
Source: "..\doc\*"; DestDir: "{app}\m3\doc"; Flags: recursesubdirs
Source: "..\lib\*"; DestDir: "{app}\m3\lib"; Flags: recursesubdirs
Source: "..\src\*"; DestDir: "{app}\m3\src"; Flags: recursesubdirs
Source: "..\test\*"; DestDir: "{app}\m3\test"; Flags: recursesubdirs

[Icons]
Name: "{group}\Sesis Command Prompt"; Filename: "{app}\m3\bin\sesis.bat"; WorkingDir: "%HOMEDRIVE%%HOMEPATH%"
Name: "{group}\Sesis Manuals"; Filename: "{app}\m3\doc\manual.pdf"
Name: "{group}\Sesis ChangeLog"; Filename: "{app}\m3\ChangeLog.txt"
Name: "{group}\Uninstall Sesis Tools"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Sesis Command Prompt"; Filename: "{app}\m3\bin\sesis.bat"; WorkingDir: "%HOMEDRIVE%%HOMEPATH%"

[Run]
Filename: "{app}\m3\bin\m3.bat"; Parameters: "*.i3"; WorkingDir: "{app}\m3\lib"

[Registry]
ROOT: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: string; ValueName: "M3_HOME"; ValueData: "{app}\m3"; FLAGS: uninsclearvalue
ROOT: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: string; ValueName: "M3_PATH"; ValueData: "{code:M3Path|}"; FLAGS: uninsclearvalue

[Code]

function M3Path(Default: String): String;
var m3, python, gs: String;
begin
  gs := ExtractFilePath(ExpandConstant('{reg:HKLM\SOFTWARE\AFPL Ghostscript\8.00,GS_DLL|}'));
  python := ExpandConstant('{reg:HKLM\SOFTWARE\Python\PythonCore\2.3\InstallPath,|}');
  m3 := ExpandConstant('{app}\m3\bin');
  Result := gs + ';' + python + ';' + m3;
end;




