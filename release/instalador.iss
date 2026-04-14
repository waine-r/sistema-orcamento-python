; =========================
; CONFIGURAÇÃO DO SISTEMA
; =========================

#define MyAppName "Sistema de Orçamentos"        ; nome do sistema
#define MyAppVersion "2.8.1"                     ; versão
#define MyAppPublisher "Herik Engenharia"        ; seu nome/empresa
#define MyAppExeName "SistemaOrcamento_v2.8.1.exe" ; nome do exe

[Setup]

; ID único do sistema (NÃO DUPLICAR)
AppId={{A1234567-B89C-1234-D567-123456789ABC}}

; nome e versão
AppName={#MyAppName}
AppVersion={#MyAppVersion}

; pasta de instalação
DefaultDirName={autopf}\SistemaOrcamento

; nome no menu iniciar
DefaultGroupName=SistemaOrcamento

; nome do instalador gerado
OutputBaseFilename=Instalador_SistemaOrcamento

; onde salvar
OutputDir=.

; compressão
Compression=lzma
SolidCompression=yes


[Files]

; pega o .exe da mesma pasta
Source: "{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion


[Icons]

; atalho menu iniciar
Name: "{group}\Sistema de Orçamentos"; Filename: "{app}\{#MyAppExeName}"

; atalho desktop
Name: "{commondesktop}\Sistema de Orçamentos"; Filename: "{app}\{#MyAppExeName}"


[Run]

; executa após instalar
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir sistema"; Flags: nowait postinstall skipifsilent