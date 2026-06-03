# Sistema de Telemetria GPS com ESP32

Projeto experimental de telemetria utilizando ESP32 para captura de localização geográfica, armazenamento em cartão SD e visualização posterior através de uma aplicação Python.

---

# Objetivo

Desenvolver uma solução de baixo custo para registro de rotas e monitoramento de deslocamentos utilizando componentes amplamente disponíveis para aplicações educacionais e prototipagem.

---

# Arquitetura da Solução

GPS NEO-6M
↓
ESP32
↓
RTC DS3231
↓
Cartão SD
↓
Arquivo CSV
↓
Aplicação Python
↓
Mapa Interativo

---

# Componentes Utilizados

## Hardware

- ESP32
- GPS NEO-6M
- RTC DS3231
- Módulo Cartão SD
- Display OLED SSD1306
- Protoboard
- Jumpers
- Bateria / Power Bank

## Software

- Arduino IDE
- Python
- SQLite
- Folium
- Pandas

---

# Estrutura do Projeto

```text
iot-telemetria
│
├── arduino
│   └── gps_logger
│
├── python
│   └── mapa_rotas
│
├── docs
│
├── imagens
│
└── exemplos

```

# Funcionalidades

- Captura de coordenadas GPS
- Registro de data e hora utilizando RTC
- Gravação automática em cartão SD
- Exibição das coordenadas em display OLED
- Importação dos dados em Python
- Visualização da rota em mapa

---

# Aplicações

- Rastreamento experimental de veículos
- Estudos de logística
- Telemetria educacional
- Projetos de IoT
- Geolocalização

---

# Status

Em desenvolvimento.

Próximas etapas:

- Publicação do código Arduino
- Publicação da aplicação Python
- Inclusão de fotos da montagem
- Inclusão de diagramas elétricos
- Inclusão de dados de exemplo

---
## Montagem do Protótipo

### Visão Geral

![Protótipo](imagens/iot-telemetria-protoboard1.png)

### Evolução da Montagem

![Etapa 2](imagens/iot-telemetria-protoboard3.png)

![Etapa 3](imagens/iot-telemetria-protoboard5.png)
---
# Autor

Luis Claudio Buratini

GitHub:
https://github.com/lcburatini
