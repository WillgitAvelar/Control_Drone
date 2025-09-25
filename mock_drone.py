
import socket
import threading
import time
import json

class MockDrone:
    def __init__(self, ip='0.0.0.0', port=8080):
        self.ip = ip
        self.port = port
        self.status = {
            'battery': 100,
            'altitude': 0,
            'speed': 0,
            'gps_signal': 5,
            'armed': False,
            'flying': False
        }
        self.server_socket = None
        self.running = False
        print(f"Drone simulado iniciado em {self.ip}:{self.port}")

    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.ip, self.port))
        print("Mock drone aguardando comandos...")
        
        while self.running:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                self.handle_command(data, addr)
            except Exception as e:
                if self.running:
                    print(f"Erro no mock drone: {e}")

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Mock drone parado.")

    def handle_command(self, data, addr):
        try:
            message = data.decode()
            if message == 'HELLO':
                print(f"Handshake recebido de {addr}")
                self.server_socket.sendto(b'OK', addr)
                return

            cmd_data = json.loads(message)
            command = cmd_data.get('cmd')
            print(f"Comando recebido: {command}")

            response = {'success': True}

            if command == 'takeoff':
                self.status['flying'] = True
                self.status['altitude'] = 10
            elif command == 'land':
                self.status['flying'] = False
                self.status['altitude'] = 0
            elif command == 'emergency_stop':
                self.status['flying'] = False
                self.status['armed'] = False
            elif command == 'get_status':
                response['status'] = self.status
            
            self.server_socket.sendto(json.dumps(response).encode(), addr)


        except Exception as e:
            print(f"Erro ao processar comando: {e}")

if __name__ == "__main__":
    drone = MockDrone()
    drone_thread = threading.Thread(target=drone.start)
    drone_thread.daemon = True
    drone_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        drone.stop()


