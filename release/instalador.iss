; =========================
; CONFIGURAÇÃO DO SISTEMA
; =========================

#define MyAppName "Sistema de Orçamentos"        ; nome do sistema
#define MyAppVersion "2.8.0"                     ; versão
#define MyAppPublisher "Herik Engenharia"        ; seu nome/empresa
#define MyAppExeName "SistemaOrcamento_v2.8.0.exe" ; nome do exe

[Setup]

; ID único do sistema (pode manter esse)
AppId={{A1234567-B89C-1234-D567-123456789ABC}}

; nome e versão
AppName={#MyAppName}
AppVersion={#MyAppVersion}

; pasta padrão de instalação (Arquivos de Programas)
DefaultDirName={autopf}\SistemaOrcamento

; nome no menu iniciar
DefaultGroupName=SistemaOrcamento

; nome do instalador gerado
OutputBaseFilename=Instalador_SistemaOrcamento

; onde salvar o instalador (mesma pasta do script)
OutputDir=.

; compressão (deixa leve)
Compression=lzma
SolidCompression=yes


[Files]

; 🔥 CAMINHO DO SEU EXE (MUITO IMPORTANTE)
; ajuste se necessário
Source: "release\SistemaOrcamento_v2.8.0.exe"; DestDir: "{app}"; Flags: ignoreversion


[Icons]

; atalho no menu iniciar
Name: "{group}\Sistema de Orçamentos"; Filename: "{app}\SistemaOrcamento_v2.8.0.exe"

; atalho na área de trabalho
Name: "{commondesktop}\Sistema de Orçamentos"; Filename: "{app}\SistemaOrcamento_v2.8.0.exe"


[Run]

; executa o sistema após instalar
Filename: "{app}\SistemaOrcamento_v2.8.0.exe"; Description: "Abrir sistema"; Flags: nowait postinstall skipifsilent