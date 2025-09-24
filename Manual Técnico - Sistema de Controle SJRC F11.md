# Manual Técnico - Sistema de Controle SJRC F11

**Autor:** Manus AI  
**Data:** Setembro 2025  
**Versão:** 1.0  

## Introdução

Este manual técnico fornece informações detalhadas sobre a implementação, arquitetura e funcionamento interno do sistema de controle para drone SJRC F11. O documento é destinado a desenvolvedores, engenheiros e técnicos que desejam compreender, modificar ou contribuir para o projeto.

## Arquitetura do Sistema

### Visão Geral da Arquitetura

O sistema segue uma arquitetura cliente-servidor moderna, onde o backend Flask atua como intermediário entre a interface web (cliente) e o drone (hardware). Esta abordagem permite separação clara de responsabilidades e facilita a manutenção e extensão do sistema.

```
[Interface Web] <--HTTP/WebSocket--> [Backend Flask] <--UDP/TCP--> [Drone SJRC F11]
```

### Componentes Principais

#### 1. Backend Flask (src/main.py)
O servidor Flask é o núcleo do sistema, responsável por:
- Servir a interface web estática
- Processar requisições HTTP da interface
- Gerenciar conexões com o drone
- Implementar a lógica de controle
- Manter logs de atividades

#### 2. Controlador de Drone (src/routes/drone_control.py)
Este módulo implementa a classe `DroneController` que encapsula toda a lógica de comunicação com o drone:

```python
class DroneController:
    def __init__(self):
        self.connected = False
        self.socket = None
        self.drone_ip = None
        self.drone_port = 8080
        self.status = {...}
```

#### 3. Interface Web (src/static/index.html)
Interface responsiva desenvolvida em HTML5/CSS3/JavaScript que oferece:
- Controles visuais intuitivos
- Feedback em tempo real
- Atalhos de teclado
- Log de atividades

### Protocolo de Comunicação

#### Estrutura de Pacotes
O protocolo SJRC F11 utiliza comunicação UDP na porta 8080 (configurável). A estrutura básica dos pacotes segue o formato:

```
[HEADER][COMMAND][PARAMETERS][CHECKSUM]
```

Onde:
- **HEADER**: Identificador do protocolo (4 bytes)
- **COMMAND**: Código do comando (2 bytes)
- **PARAMETERS**: Dados específicos do comando (variável)
- **CHECKSUM**: Validação de integridade (2 bytes)

#### Comandos Implementados

| Comando | Código | Parâmetros | Descrição |
|---------|--------|------------|-----------|
| HELLO | 0x01 | Nenhum | Handshake inicial |
| TAKEOFF | 0x02 | Altitude | Comando de decolagem |
| LAND | 0x03 | Nenhum | Comando de pouso |
| MOVE | 0x04 | Direção, Velocidade | Movimento direcional |
| ROTATE | 0x05 | Direção, Ângulo | Rotação |
| EMERGENCY | 0xFF | Nenhum | Parada de emergência |

### API REST

#### Endpoints Disponíveis

##### POST /api/drone/connect
Estabelece conexão com o drone.

**Parâmetros:**
```json
{
  "ip_address": "192.168.4.1"
}
```

**Resposta:**
```json
{
  "status": "connected",
  "ip": "192.168.4.1"
}
```

##### POST /api/drone/disconnect
Encerra conexão com o drone.

**Resposta:**
```json
{
  "status": "disconnected"
}
```

##### GET /api/drone/status
Obtém status atual do drone.

**Resposta:**
```json
{
  "connected": true,
  "status": {
    "battery": 85,
    "altitude": 10,
    "speed": 5,
    "gps_signal": 8,
    "armed": true,
    "flying": true
  }
}
```

##### POST /api/drone/takeoff
Comando de decolagem.

**Resposta:**
```json
{
  "success": true,
  "response": "Takeoff initiated"
}
```

##### POST /api/drone/land
Comando de pouso.

**Resposta:**
```json
{
  "success": true,
  "response": "Landing initiated"
}
```

##### POST /api/drone/move
Comando de movimento.

**Parâmetros:**
```json
{
  "direction": "forward",
  "speed": 50
}
```

**Resposta:**
```json
{
  "success": true,
  "response": "Movement command sent"
}
```

##### POST /api/drone/rotate
Comando de rotação.

**Parâmetros:**
```json
{
  "direction": "clockwise",
  "angle": 90
}
```

**Resposta:**
```json
{
  "success": true,
  "response": "Rotation command sent"
}
```

##### POST /api/drone/emergency_stop
Parada de emergência.

**Resposta:**
```json
{
  "success": true,
  "response": "Emergency stop activated"
}
```

## Implementação Detalhada

### Gerenciamento de Conexão

A conexão com o drone é gerenciada através de sockets UDP Python:

```python
def connect(self, ip_address):
    try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        self.drone_ip = ip_address
        
        # Handshake
        test_command = b'HELLO'
        self.socket.sendto(test_command, (self.drone_ip, self.drone_port))
        
        response, addr = self.socket.recvfrom(1024)
        
        if response:
            self.connected = True
            return True
    except Exception as e:
        self.connected = False
        return False
```

### Envio de Comandos

Os comandos são enviados como objetos JSON serializados:

```python
def send_command(self, command, params=None):
    if not self.connected:
        return {'error': 'Drone não conectado'}
        
    try:
        cmd_data = {
            'cmd': command,
            'params': params or {}
        }
        
        message = json.dumps(cmd_data).encode()
        self.socket.sendto(message, (self.drone_ip, self.drone_port))
        
        response, addr = self.socket.recvfrom(1024)
        return {'success': True, 'response': response.decode()}
        
    except Exception as e:
        return {'error': str(e)}
```

### Interface JavaScript

A interface web utiliza fetch API para comunicação assíncrona:

```javascript
async function connectDrone() {
    const ip = document.getElementById('droneIp').value;
    
    try {
        const response = await fetch('/api/drone/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip_address: ip })
        });
        
        const result = await response.json();
        
        if (result.status === 'connected') {
            isConnected = true;
            updateConnectionStatus('Conectado', 'connected');
            startStatusUpdates();
        }
    } catch (error) {
        addLog(`Erro de rede: ${error.message}`, 'error');
    }
}
```

## Engenharia Reversa

### Ferramenta de Análise

O projeto inclui uma ferramenta especializada para engenharia reversa do protocolo:

```python
class PacketCapture:
    def __init__(self, interface='wlan0'):
        self.interface = interface
        self.packets = []
        self.running = False
        
    def start_capture(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        sock.bind(('', 0))
        
        while self.running:
            data, addr = sock.recvfrom(65535)
            packet_info = {
                'timestamp': datetime.now().isoformat(),
                'source': addr[0],
                'data_length': len(data),
                'data_hex': data.hex(),
                'data_ascii': self._to_ascii(data)
            }
            self.packets.append(packet_info)
```

### Análise de Padrões

A ferramenta implementa análise automática de padrões:

```python
def analyze_patterns(self):
    # Análise por tamanho
    sizes = {}
    for packet in self.packets:
        size = packet['data_length']
        sizes[size] = sizes.get(size, 0) + 1
    
    # Análise por origem
    sources = {}
    for packet in self.packets:
        source = packet['source']
        sources[source] = sources.get(source, 0) + 1
    
    # Padrões comuns
    common_prefixes = {}
    for packet in self.packets:
        hex_data = packet['data_hex']
        if len(hex_data) >= 8:
            prefix = hex_data[:8]
            common_prefixes[prefix] = common_prefixes.get(prefix, 0) + 1
```

### Metodologia de Decifração

1. **Captura de Tráfego**: Use Wireshark ou a ferramenta incluída para capturar pacotes entre o app móvel e o drone
2. **Isolamento de Comandos**: Execute comandos específicos no app e identifique os pacotes correspondentes
3. **Análise de Estrutura**: Compare pacotes similares para identificar campos fixos e variáveis
4. **Validação**: Implemente os comandos decifrados e teste com o drone
5. **Documentação**: Documente a estrutura descoberta para futura referência

## Configuração de Desenvolvimento

### Ambiente de Desenvolvimento

Para configurar o ambiente de desenvolvimento:

```bash
# Clone o projeto
git clone <repository-url>
cd sjrc-f11-controller

# Ative o ambiente virtual
source venv/bin/activate

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt

# Execute testes
python -m pytest tests/

# Inicie em modo debug
export FLASK_ENV=development
python src/main.py
```

### Estrutura de Testes

```
tests/
├── test_drone_controller.py    # Testes do controlador
├── test_api_endpoints.py       # Testes da API
├── test_packet_analysis.py     # Testes de engenharia reversa
└── fixtures/
    ├── sample_packets.json     # Pacotes de exemplo
    └── mock_responses.json     # Respostas simuladas
```

### Debugging

Para debugging avançado, configure logs detalhados:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('drone_controller.log'),
        logging.StreamHandler()
    ]
)
```

## Otimização e Performance

### Otimizações de Rede

- Use connection pooling para múltiplas conexões
- Implemente retry logic com backoff exponencial
- Configure timeouts apropriados para diferentes tipos de comando
- Use compressão de dados quando possível

### Otimizações de Interface

- Implemente debouncing para controles de movimento
- Use Web Workers para processamento pesado
- Otimize atualizações de DOM com requestAnimationFrame
- Implemente cache local para configurações

### Monitoramento

Implemente métricas de performance:

```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper
```

## Segurança

### Validação de Entrada

Sempre valide dados de entrada:

```python
def validate_movement_command(direction, speed):
    valid_directions = ['forward', 'backward', 'left', 'right', 'up', 'down']
    if direction not in valid_directions:
        raise ValueError(f"Invalid direction: {direction}")
    
    if not 0 <= speed <= 100:
        raise ValueError(f"Speed must be between 0-100: {speed}")
```

### Autenticação

Para ambientes de produção, implemente autenticação:

```python
from functools import wraps
from flask import request, jsonify

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function
```

### Rate Limiting

Implemente rate limiting para prevenir spam:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/drone/move', methods=['POST'])
@limiter.limit("10 per minute")
def move():
    # Implementação do movimento
    pass
```

## Troubleshooting

### Problemas Comuns

#### Erro de Conexão
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Solução:**
- Verifique se o drone está ligado
- Confirme a conexão Wi-Fi
- Teste conectividade com ping

#### Timeout de Socket
```
socket.timeout: timed out
```

**Solução:**
- Aumente o timeout do socket
- Verifique a qualidade do sinal Wi-Fi
- Reduza a distância do drone

#### Comandos Ignorados
```
{'error': 'Command not recognized'}
```

**Solução:**
- Verifique se o protocolo foi corretamente implementado
- Analise logs de comunicação
- Compare com tráfego do app oficial

### Logs de Debug

Configure logs detalhados para troubleshooting:

```python
logger = logging.getLogger(__name__)

def send_command(self, command, params=None):
    logger.debug(f"Sending command: {command} with params: {params}")
    
    try:
        # Implementação
        logger.debug(f"Command sent successfully")
    except Exception as e:
        logger.error(f"Failed to send command: {e}")
```

## Extensões Futuras

### Suporte a Múltiplos Drones

```python
class MultiDroneController:
    def __init__(self):
        self.drones = {}
    
    def add_drone(self, drone_id, ip_address):
        self.drones[drone_id] = DroneController()
        self.drones[drone_id].connect(ip_address)
    
    def send_command_to_all(self, command, params=None):
        results = {}
        for drone_id, controller in self.drones.items():
            results[drone_id] = controller.send_command(command, params)
        return results
```

### Integração com Sistemas Externos

```python
class TelemetryIntegration:
    def __init__(self, mqtt_broker):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(mqtt_broker)
    
    def publish_telemetry(self, drone_status):
        payload = json.dumps(drone_status)
        self.mqtt_client.publish("drone/telemetry", payload)
```

### Interface de Programação de Voos

```python
class FlightProgrammer:
    def __init__(self, drone_controller):
        self.drone = drone_controller
        self.waypoints = []
    
    def add_waypoint(self, lat, lon, altitude, action=None):
        waypoint = {
            'lat': lat,
            'lon': lon,
            'altitude': altitude,
            'action': action
        }
        self.waypoints.append(waypoint)
    
    def execute_flight_plan(self):
        for waypoint in self.waypoints:
            self.fly_to_waypoint(waypoint)
```

## Conclusão

Este manual técnico fornece uma visão abrangente da implementação do sistema de controle para drone SJRC F11. A arquitetura modular e bem documentada facilita a manutenção, extensão e contribuição ao projeto.

Para questões técnicas específicas ou contribuições, consulte a documentação adicional no repositório do projeto ou entre em contato com a comunidade de desenvolvedores.

---

**Nota:** Este documento é atualizado regularmente conforme o projeto evolui. Consulte sempre a versão mais recente para informações atualizadas.

