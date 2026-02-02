# Informacoes do Sistema - PC Igor Vasconcelos

> **ARQUIVO DE REFERENCIA PARA CLAUDE CODE**
> Este arquivo contem todas as especificacoes tecnicas do computador.
> Leia este arquivo quando precisar de informacoes sobre hardware, software, drivers ou configuracoes do sistema.
> Ultima atualizacao: 2026-01-08

---

## Resumo Executivo

| Componente | Especificacao |
|------------|---------------|
| **Nome do Host** | IGORVASCONCELOS |
| **Sistema Operacional** | Windows 11 Pro (Build 26200) |
| **Processador** | AMD Ryzen 9 7900 (12 cores / 24 threads) @ 3.7GHz |
| **Memoria RAM** | 64GB DDR5 (2x 32GB Kingston @ 3600MHz) |
| **GPU Principal** | NVIDIA GeForce RTX 3060 Ti (8GB) |
| **GPU Integrada** | AMD Radeon Graphics |
| **Armazenamento** | Kingston KC3000 1TB NVMe SSD |
| **Placa-Mae** | ASUS PRIME B650M-A II |

---

## 1. Sistema Operacional

### Informacoes Gerais
- **Nome**: Microsoft Windows 11 Pro
- **Versao**: 10.0.26200 (Build 26200)
- **Arquitetura**: 64-bit (x64-based PC)
- **Data de Instalacao**: 01/05/2025
- **Diretorio Windows**: C:\WINDOWS
- **Diretorio System32**: C:\WINDOWS\system32
- **Localidade**: pt-BR (Portugues Brasil)
- **Fuso Horario**: UTC-03:00 (Brasilia)

### Hotfixes Instalados
| KB | Descricao |
|----|-----------|
| KB5067931 | Atualizacao de seguranca |
| KB5054156 | Atualizacao de seguranca |
| KB5072033 | Atualizacao de seguranca |
| KB5071142 | Atualizacao de seguranca |

### Seguranca Baseada em Virtualizacao
- **Status**: Executando
- **Servicos Ativos**:
  - Integridade de Codigo imposta por Hypervisor
  - Protecao de Pilha Imposta por Hardware no Modo Kernel
- **App Control for Business**: Imposto

---

## 2. Processador (CPU)

### Especificacoes
| Propriedade | Valor |
|-------------|-------|
| **Modelo** | AMD Ryzen 9 7900 12-Core Processor |
| **Fabricante** | AuthenticAMD |
| **Familia/Modelo** | Family 25 Model 97 Stepping 2 |
| **Nucleos Fisicos** | 12 |
| **Threads (Logicos)** | 24 |
| **Clock Base** | 3701 MHz (3.7 GHz) |
| **Cache L2** | 12 MB (12288 KB) |
| **Cache L3** | 64 MB (65536 KB) |
| **Arquitetura** | Zen 4 (AMD64) |

### Notas Tecnicas
- Processador de alto desempenho da serie Ryzen 9
- Suporte a DDR5, PCIe 5.0
- TDP: 65W (Eco) / 88W (PPT)
- Tecnologias: SMT, Precision Boost 2, AMD EXPO

---

## 3. Memoria RAM

### Configuracao Total
- **Memoria Fisica Total**: 64 GB (67.801.604.096 bytes)
- **Tipo**: DDR5
- **Configuracao**: Dual Channel

### Modulos Instalados
| Slot | Fabricante | Part Number | Capacidade | Velocidade JEDEC | Clock Configurado |
|------|------------|-------------|------------|------------------|-------------------|
| DIMM 0 | Kingston | KF556C40-32 | 32 GB | 4800 MHz | 3600 MHz |
| DIMM 1 | Kingston | KF556C36-32 | 32 GB | 4800 MHz | 3600 MHz |

### Memoria Virtual
- **Tamanho Maximo**: 68.757 MB
- **Arquivo de Paginacao**: C:\pagefile.sys

### Notas Tecnicas
- Memoria Kingston Fury DDR5 de alta performance
- XMP/EXPO pode estar ativado (3600MHz vs 4800MHz JEDEC)
- Para habilitar velocidade total, verificar BIOS/EXPO

---

## 4. Placa-Mae (Motherboard)

### Especificacoes
| Propriedade | Valor |
|-------------|-------|
| **Fabricante** | ASUSTeK COMPUTER INC. |
| **Modelo** | PRIME B650M-A II |
| **Versao** | Rev 1.xx |
| **Serial** | 230114853301913 |
| **Formato** | Micro-ATX |

### BIOS
| Propriedade | Valor |
|-------------|-------|
| **Fabricante** | American Megatrends Inc. |
| **Versao** | 3024 |
| **Data** | 01/08/2024 |
| **Tipo** | UEFI |

### Recursos da Placa-Mae
- Chipset AMD B650
- Socket AM5
- Suporte PCIe 4.0/5.0
- USB 3.2 Gen 2
- Realtek 2.5GbE LAN
- Iluminacao Aura Sync

---

## 5. Placas de Video (GPU)

### GPU Dedicada Principal
| Propriedade | Valor |
|-------------|-------|
| **Modelo** | NVIDIA GeForce RTX 3060 Ti |
| **VRAM** | 8 GB GDDR6 (4.293.918.720 bytes reportados) |
| **Driver** | 32.0.15.6636 |
| **Data do Driver** | 02/12/2024 |
| **Status** | OK |
| **Arquitetura** | Ampere (GA104) |

### GPU Integrada (iGPU)
| Propriedade | Valor |
|-------------|-------|
| **Modelo** | AMD Radeon Graphics |
| **Processador** | AMD Radeon Graphics Processor (0x164E) |
| **Driver** | 32.0.21037.1004 |
| **Data do Driver** | 27/11/2025 |
| **Resolucao Ativa** | 3840 x 2160 @ 59Hz (4K) |
| **Status** | OK |

### Monitor Virtual Desktop
| Propriedade | Valor |
|-------------|-------|
| **Modelo** | Virtual Desktop Monitor |
| **Driver** | 10.54.50.446 |
| **Status** | Error (normal quando VR nao esta em uso) |

### Notas Tecnicas
- RTX 3060 Ti: Excelente para jogos 1440p/4K e trabalhos com IA/CUDA
- iGPU AMD pode ser usada para displays secundarios ou encoding
- Driver NVIDIA pode ser atualizado via GeForce Experience

---

## 6. Armazenamento

### Disco Principal
| Propriedade | Valor |
|-------------|-------|
| **Modelo** | Kingston SKC3000S1024G |
| **Tipo** | NVMe SSD (M.2) |
| **Capacidade** | 1 TB (1.024.203.640.320 bytes) |
| **Interface** | SCSI (NVMe) |
| **Status** | OK |

### Volumes/Particoes
| Drive | Sistema de Arquivos | Tipo | Tamanho Total | Espaco Livre | Status |
|-------|---------------------|------|---------------|--------------|--------|
| C: | NTFS | Fixed | 952 GB | ~47 GB | Healthy |
| (Sistema) | NTFS | Fixed | 875 MB | ~75 MB | Healthy |

### Notas Tecnicas
- Kingston KC3000: SSD PCIe 4.0 de alta performance (ate 7000 MB/s)
- **ATENCAO**: Espaco livre no C: esta baixo (~47 GB). Considerar limpeza.
- Particao de sistema EFI presente e saudavel

---

## 7. Rede

### Adaptadores de Rede
| Nome | Descricao | Status | MAC Address | Velocidade |
|------|-----------|--------|-------------|------------|
| Wi-Fi 4 | Intel Dual Band Wireless-AC 7260 | Up (Conectado) | 6C-29-95-99-C1-BD | 1 Gbps |
| Ethernet | Realtek Gaming 2.5GbE Family Controller | Disconnected | C8-7F-54-A8-33-AF | - |
| Bluetooth | Bluetooth Device (PAN) | Disconnected | F4-4E-FC-97-A8-8C | - |
| OpenVPN | Surfshark VPN Data Channel | Disconnected | - | - |

### Configuracao IP (Wi-Fi Ativo)
| Propriedade | Valor |
|-------------|-------|
| **Interface** | Wi-Fi 4 |
| **IPv4** | 192.168.0.235 |
| **DHCP** | Ativado |
| **Servidor DHCP** | 192.168.0.1 |
| **Gateway Padrao** | 192.168.0.1 |

### VPN
- Surfshark instalado (OpenVPN Data Channel Offload)
- Atualmente desconectado

---

## 8. Audio

### Dispositivos de Audio
| Dispositivo | Status |
|-------------|--------|
| AMD High Definition Audio Device | OK |
| Realtek High Definition Audio | OK |
| NVIDIA High Definition Audio | OK |
| AMD Streaming Audio Device | OK |
| Steam Streaming Microphone | OK |
| Steam Streaming Speakers | OK |
| NVIDIA Virtual Audio Device (WDM) | OK |
| Virtual Desktop Audio | OK |
| ASUS Utility | OK |

### Notas Tecnicas
- Multiplas saidas de audio disponiveis (HDMI via GPU, Realtek onboard)
- Dispositivos virtuais para streaming (Steam, VR)

---

## 9. Programas de Inicializacao (Startup)

| Programa | Comando/Localizacao |
|----------|---------------------|
| AMD Noise Suppression | C:\WINDOWS\system32\AMD\ANR\AMDNoiseSuppression.exe |
| Ollama | Ollama.lnk |
| Monica AI | C:\Users\IgorPC\AppData\Local\Programs\Monica\Monica.exe |
| Epson Printer | E_YATIYOE.EXE |
| OneDrive | C:\Program Files\Microsoft OneDrive\OneDrive.exe /background |
| Microsoft Lists | OneDrive integration |
| Opera Browser | C:\Users\IgorPC\AppData\Local\Programs\Opera\opera.exe |
| Figma Agent | C:\Users\IgorPC\AppData\Local\FigmaAgent\figma_agent.exe |
| Epic Games Launcher | Portal\Binaries |
| Surfshark VPN | C:\Program Files\Surfshark\Surfshark.exe |
| LM Studio | C:\Users\IgorPC\AppData\Local\Programs\LM Studio\LM Studio.exe |
| Proton Drive | C:\Users\IgorPC\AppData\Local\Programs\Proton\Drive |
| Perplexity | com.todesktop.25020447d4kq915 |
| Microsoft Edge | C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe |
| Microsoft Teams | WindowsApps\MSTeam |
| PDFelement | PENotify.exe |
| Windows Security | SecurityHealthSystray.exe |
| XP-Pen Tablet | C:\Program Files\XPPen\PenTablet.exe /mini |
| Epson Printer Connection | EPPCCMON |
| Realtek Audio Service | RtkAudUService |

---

## 10. Software Instalado (Principais)

### Desenvolvimento
| Software | Versao |
|----------|--------|
| Node.js | 24.12.0 |
| Python 3.14 | 3.14.2150.0 |
| Python 3.12 | 3.12.9150.0 |
| PowerShell 7 | 7.5.4.0 |
| Git | (instalado via PATH) |
| Visual Studio Build Tools | 17.14.x |
| Windows SDK | 10.1.26100.7175 |

### Microsoft Visual C++ Redistributables
| Versao | Arquitetura |
|--------|-------------|
| VC++ 2005 | x64, x86 |
| VC++ 2008 | x64, x86 |
| VC++ 2010 | x64, x86 |
| VC++ 2012 | x64, x86 |
| VC++ 2013 | x64, x86 |
| VC++ 2022 | x64, x86 |

### .NET Runtimes
| Runtime | Versao |
|---------|--------|
| .NET 6.0 Runtime | 6.0.16, 6.0.36 |
| .NET 8.0 Runtime | 8.0.13, 8.0.22 |
| .NET Windows Desktop 8.0 | 8.0.22 |
| ASP.NET Core 8.0 | 8.0.22 |

### Jogos/Launchers
| Software | Versao |
|----------|--------|
| Epic Games Launcher | 1.3.93.0 |
| Paradox Launcher v2 | 2.4.0 |
| REDlauncher (CD Projekt) | 3.4.0.5 |
| Virtual Desktop | 1.30.1 |
| Virtual Desktop Service | 1.18.42 |

### Produtividade
| Software | Versao |
|----------|--------|
| Microsoft Office (Click-to-Run) | 16.0.19426.20170 |
| Microsoft Teams Add-in | 1.24.19202 |
| Bizagi Modeler | 4.0.0112 |
| WinDirStat | 2.2.2 |
| Proton Drive | 1.9.0 |

### Hardware/Drivers
| Software | Versao |
|----------|--------|
| AMD Install Manager | 25.20.25315.0337 |
| AMD Settings | 2025.1128.1346.2068 |
| AMD Chipset Drivers | 7.11.26.2142 |
| Intel Wireless Bluetooth | 19.71.0 |
| Intel PRO/Wireless WiFi | 21.10.1.3139 |
| Intel Driver Assistant | 25.4.36.6 |
| ASUS Aura Service | 3.08.59 |
| ROG Live Service | 3.3.16.0 |
| Logitech Plugin Service | 6.2.6.1611 |
| XP-Pen Tablet | (instalado) |

### Impressora
| Software | Versao |
|----------|--------|
| HP LaserJet Pro M428f-M429f | 48.6.4638.2245 |
| Epson Scan/Print Software | Varios |
| Epson Connect Printer Setup | 1.4.9 |

### Seguranca/VPN
| Software | Versao |
|----------|--------|
| Surfshark | 5.12.2.999 |

### IA/ML
| Software | Versao |
|----------|--------|
| Ollama | (startup) |
| LM Studio | (startup) |

---

## 11. Variaveis de Ambiente

### Variaveis do Sistema
| Variavel | Valor |
|----------|-------|
| COMPUTERNAME | IGORVASCONCELOS |
| OS | Windows_NT |
| PROCESSOR_ARCHITECTURE | AMD64 |
| NUMBER_OF_PROCESSORS | 24 |
| SYSTEMROOT | C:\WINDOWS |
| SYSTEMDRIVE | C: |
| COMSPEC | C:\WINDOWS\system32\cmd.exe |
| TEMP / TMP | C:\Users\IgorPC\AppData\Local\Temp |

### Variaveis do Usuario
| Variavel | Valor |
|----------|-------|
| USERNAME | IgorPC |
| USERPROFILE | C:\Users\IgorPC |
| HOMEPATH | \Users\IgorPC |
| APPDATA | C:\Users\IgorPC\AppData\Roaming |
| LOCALAPPDATA | C:\Users\IgorPC\AppData\Local |
| OneDrive | C:\Users\IgorPC\OneDrive |

### Variaveis de Desenvolvimento
| Variavel | Valor |
|----------|-------|
| ChocolateyInstall | C:\ProgramData\chocolatey |
| GIT_EDITOR | true |
| SHELL | C:\Program Files\Git\usr\bin\bash.exe |
| LANG | pt_BR.UTF-8 |
| TERM | xterm-256color |

### PATH do Sistema (Principais Entradas)
```
C:\Python314\Scripts
C:\Python314
C:\Python312\Scripts
C:\Python312
C:\WINDOWS\system32
C:\WINDOWS
C:\Program Files\dotnet
C:\Program Files\Git\cmd
C:\Program Files\PowerShell\7
C:\Program Files\nodejs
C:\ProgramData\chocolatey\bin
C:\Program Files\Intel\WiFi\bin
C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common
C:\Program Files\NVIDIA Corporation\NVIDIA app\NvDLISR
```

### PATH do Usuario (Principais Entradas)
```
C:\Users\IgorPC\AppData\Local\Microsoft\WindowsApps
C:\Users\IgorPC\AppData\Local\Programs\Microsoft VS Code\bin
C:\Users\IgorPC\.lmstudio\bin
C:\Users\IgorPC\AppData\Local\Programs\Ollama
C:\Users\IgorPC\AppData\Local\Microsoft\WinGet\Links
C:\Users\IgorPC\AppData\Local\Programs\Antigravity\bin
C:\Users\IgorPC\AppData\Roaming\npm
C:\Users\IgorPC\.local\bin
```

---

## 12. Informacoes de Diagnostico

### Comandos Uteis para Diagnostico

#### Hardware
```powershell
# Informacoes gerais do sistema
systeminfo

# CPU detalhada
wmic cpu get name,numberofcores,numberoflogicalprocessors,maxclockspeed

# Memoria RAM
wmic memorychip get manufacturer,capacity,speed,partnumber

# Discos
wmic diskdrive get model,size,status

# GPU
wmic path win32_videocontroller get name,driverversion,adapterram
```

#### Rede
```powershell
# Configuracao IP
ipconfig /all

# Teste de conectividade
ping google.com

# Rota de rede
tracert google.com

# DNS Cache
ipconfig /displaydns

# Reset de rede
netsh winsock reset
netsh int ip reset
```

#### Sistema
```powershell
# Verificar arquivos do sistema
sfc /scannow

# Verificar imagem do Windows
DISM /Online /Cleanup-Image /CheckHealth
DISM /Online /Cleanup-Image /ScanHealth
DISM /Online /Cleanup-Image /RestoreHealth

# Verificar disco
chkdsk C: /f /r

# Eventos do sistema
eventvwr.msc
```

#### Performance
```powershell
# Monitor de recursos
resmon

# Gerenciador de tarefas avancado
taskmgr

# Informacoes de performance
perfmon
```

### Problemas Comuns e Solucoes

#### Espaco em Disco Baixo
O drive C: esta com aproximadamente 47 GB livres. Acoes recomendadas:
1. Executar Limpeza de Disco: `cleanmgr`
2. Limpar cache do Windows Update
3. Verificar pasta Temp: `%TEMP%`
4. Usar WinDirStat para identificar arquivos grandes

#### Drivers
- **NVIDIA**: Atualizar via GeForce Experience ou site oficial
- **AMD (Chipset/GPU)**: Usar AMD Software: Adrenalin Edition
- **Intel WiFi**: Intel Driver & Support Assistant instalado

#### Atualizacoes
- Windows Update: Configuracoes > Windows Update
- Drivers: Device Manager ou software do fabricante
- BIOS: Verificar site ASUS para PRIME B650M-A II

---

## 13. Contatos e Links Uteis

### Downloads de Drivers
- **ASUS (Placa-Mae)**: https://www.asus.com/motherboards-components/motherboards/prime/prime-b650m-a-ii/helpdesk_download/
- **NVIDIA (GPU)**: https://www.nvidia.com/Download/index.aspx
- **AMD (Chipset)**: https://www.amd.com/en/support
- **Intel (WiFi/Bluetooth)**: https://www.intel.com/content/www/us/en/support.html

### Suporte
- **ASUS**: https://www.asus.com/support/
- **Kingston (RAM/SSD)**: https://www.kingston.com/support

---

## Notas Finais

Este documento foi gerado automaticamente em 2026-01-08 e contem as especificacoes tecnicas completas do computador de Igor Vasconcelos.

**Para Claude Code**: Este arquivo deve ser consultado quando:
- O usuario perguntar sobre especificacoes do computador
- For necessario diagnosticar problemas de hardware ou software
- For necessario verificar compatibilidade de software
- For necessario sugerir otimizacoes ou upgrades
- For necessario executar comandos especificos do sistema

**Localizacao deste arquivo**: `C:\Users\IgorPC\.claude\CLAUDE_PC_SYSTEM_INFO.md`
