from flask import Blueprint, request, jsonify
import socket
import threading
import time
import json

drone_bp = Blueprint('drone', __name__)

class DroneController:
    def __init__(self):
        self.connected = False
        self.socket = None
        self.drone_ip = None
        self.drone_port = 8080  # Porta padrão comum para drones
        self.status = {
            'battery': 0,
            'altitude': 0,
            'speed': 0,
            'gps_signal': 0,
            'armed': False,
            'flying': False
        }
        
    def connect(self, ip_address):
        """Conecta ao drone via Wi-Fi"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(5)
            self.drone_ip = ip_address
            
            # Tenta enviar um comando de handshake
            test_command = b'HELLO'
            self.socket.sendto(test_command, (self.drone_ip, self.drone_port))
            
            # Aguarda resposta
            response, addr = self.socket.recvfrom(1024)
            
            if response:
                self.connected = True
                return True
                
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.connected = False
            return False
            
    def disconnect(self):
        """Desconecta do drone"""
        if self.socket:
            self.socket.close()
        self.connected = False
        
    def send_command(self, command, params=None):
        """Envia comando para o drone"""
        if not self.connected:
            return {'error': 'Drone não conectado'}
            
        try:
            # Formato básico de comando (será refinado após engenharia reversa)
            cmd_data = {
                'cmd': command,
                'params': params or {}
            }
            
            message = json.dumps(cmd_data).encode()
            self.socket.sendto(message, (self.drone_ip, self.drone_port))
            
            # Aguarda resposta
            response, addr = self.socket.recvfrom(1024)
            return {'success': True, 'response': response.decode()}
            
        except Exception as e:
            return {'error': str(e)}

# Instância global do controlador
drone_controller = DroneController()

@drone_bp.route('/connect', methods=['POST'])
def connect_drone():
    """Conecta ao drone"""
    data = request.get_json()
    ip_address = data.get('ip_address', '192.168.4.1')  # IP padrão comum para drones
    
    success = drone_controller.connect(ip_address)
    
    if success:
        return jsonify({'status': 'connected', 'ip': ip_address})
    else:
        return jsonify({'status': 'failed', 'error': 'Não foi possível conectar ao drone'}), 400

@drone_bp.route('/disconnect', methods=['POST'])
def disconnect_drone():
    """Desconecta do drone"""
    drone_controller.disconnect()
    return jsonify({'status': 'disconnected'})

@drone_bp.route('/status', methods=['GET'])
def get_status():
    """Obtém status do drone"""
    return jsonify({
        'connected': drone_controller.connected,
        'status': drone_controller.status
    })

@drone_bp.route('/takeoff', methods=['POST'])
def takeoff():
    """Comando de decolagem"""
    result = drone_controller.send_command('takeoff')
    return jsonify(result)

@drone_bp.route('/land', methods=['POST'])
def land():
    """Comando de pouso"""
    result = drone_controller.send_command('land')
    return jsonify(result)

@drone_bp.route('/move', methods=['POST'])
def move():
    """Comando de movimento"""
    data = request.get_json()
    direction = data.get('direction')  # forward, backward, left, right, up, down
    speed = data.get('speed', 50)  # velocidade de 0-100
    
    result = drone_controller.send_command('move', {
        'direction': direction,
        'speed': speed
    })
    return jsonify(result)

@drone_bp.route('/rotate', methods=['POST'])
def rotate():
    """Comando de rotação"""
    data = request.get_json()
    direction = data.get('direction')  # clockwise, counterclockwise
    angle = data.get('angle', 90)  # ângulo em graus
    
    result = drone_controller.send_command('rotate', {
        'direction': direction,
        'angle': angle
    })
    return jsonify(result)

@drone_bp.route('/emergency_stop', methods=['POST'])
def emergency_stop():
    """Comando de parada de emergência"""
    result = drone_controller.send_command('emergency_stop')
    return jsonify(result)

