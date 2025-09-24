#!/usr/bin/env python3
"""
Ferramenta de Engenharia Reversa para SJRC F11
===============================================

Esta ferramenta ajuda na captura e análise do tráfego de rede entre
o aplicativo móvel oficial e o drone SJRC F11 para decifrar o protocolo
de comunicação.

Requisitos:
- Wireshark instalado
- Acesso ao ponto de acesso Wi-Fi do drone
- Aplicativo móvel oficial do SJRC F11

Uso:
1. Configure seu computador como ponto de acesso Wi-Fi
2. Conecte o drone e o dispositivo móvel ao seu hotspot
3. Execute esta ferramenta para capturar pacotes
4. Use o aplicativo móvel para enviar comandos ao drone
5. Analise os pacotes capturados para identificar padrões

Autor: Manus AI
Data: 2025
"""

import socket
import threading
import time
import json
import struct
from datetime import datetime
import argparse
import sys

class PacketCapture:
    def __init__(self, interface='wlan0'):
        self.interface = interface
        self.packets = []
        self.running = False
        
    def start_capture(self):
        """Inicia a captura de pacotes"""
        print(f"[{datetime.now()}] Iniciando captura na interface {self.interface}")
        print("AVISO: Esta é uma implementação básica. Para captura completa,")
        print("recomenda-se usar Wireshark com os seguintes filtros:")
        print("- ip.addr == 192.168.4.1 (IP padrão do drone)")
        print("- udp.port == 8080 or tcp.port == 8080")
        print("- wifi (para capturar todo o tráfego Wi-Fi)")
        
        self.running = True
        
        # Simulação de captura - em implementação real, usaria scapy ou similar
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
            sock.bind(('', 0))
            
            while self.running:
                try:
                    data, addr = sock.recvfrom(65535)
                    packet_info = {
                        'timestamp': datetime.now().isoformat(),
                        'source': addr[0] if addr else 'unknown',
                        'data_length': len(data),
                        'data_hex': data.hex(),
                        'data_ascii': self._to_ascii(data)
                    }
                    self.packets.append(packet_info)
                    print(f"Pacote capturado: {addr[0] if addr else 'unknown'} -> {len(data)} bytes")
                    
                except socket.error as e:
                    if self.running:
                        print(f"Erro na captura: {e}")
                    break
                    
        except PermissionError:
            print("ERRO: Permissões insuficientes para captura raw.")
            print("Execute como root ou use Wireshark para captura completa.")
            
    def stop_capture(self):
        """Para a captura de pacotes"""
        self.running = False
        print(f"[{datetime.now()}] Captura interrompida")
        
    def _to_ascii(self, data):
        """Converte dados binários para ASCII legível"""
        return ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
        
    def save_packets(self, filename):
        """Salva os pacotes capturados em arquivo JSON"""
        with open(filename, 'w') as f:
            json.dump(self.packets, f, indent=2)
        print(f"Pacotes salvos em: {filename}")
        
    def analyze_patterns(self):
        """Analisa padrões nos pacotes capturados"""
        if not self.packets:
            print("Nenhum pacote capturado para análise")
            return
            
        print(f"\n=== ANÁLISE DE {len(self.packets)} PACOTES ===")
        
        # Análise por tamanho
        sizes = {}
        for packet in self.packets:
            size = packet['data_length']
            sizes[size] = sizes.get(size, 0) + 1
            
        print("\nDistribuição por tamanho:")
        for size, count in sorted(sizes.items()):
            print(f"  {size} bytes: {count} pacotes")
            
        # Análise por origem
        sources = {}
        for packet in self.packets:
            source = packet['source']
            sources[source] = sources.get(source, 0) + 1
            
        print("\nDistribuição por origem:")
        for source, count in sorted(sources.items()):
            print(f"  {source}: {count} pacotes")
            
        # Procura por padrões comuns
        print("\nPadrões identificados:")
        common_prefixes = {}
        for packet in self.packets:
            hex_data = packet['data_hex']
            if len(hex_data) >= 8:  # Primeiros 4 bytes
                prefix = hex_data[:8]
                common_prefixes[prefix] = common_prefixes.get(prefix, 0) + 1
                
        for prefix, count in sorted(common_prefixes.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  Prefixo {prefix}: {count} ocorrências")

class DroneProtocolAnalyzer:
    """Analisador específico para protocolo SJRC F11"""
    
    def __init__(self):
        self.command_patterns = {
            'takeoff': [],
            'land': [],
            'move_forward': [],
            'move_backward': [],
            'move_left': [],
            'move_right': [],
            'move_up': [],
            'move_down': [],
            'rotate_cw': [],
            'rotate_ccw': [],
            'emergency_stop': []
        }
        
    def add_command_sample(self, command_type, packet_data):
        """Adiciona amostra de comando para análise"""
        if command_type in self.command_patterns:
            self.command_patterns[command_type].append(packet_data)
            print(f"Amostra adicionada para comando: {command_type}")
        else:
            print(f"Tipo de comando desconhecido: {command_type}")
            
    def analyze_command_structure(self):
        """Analisa a estrutura dos comandos"""
        print("\n=== ANÁLISE DE ESTRUTURA DOS COMANDOS ===")
        
        for command, samples in self.command_patterns.items():
            if not samples:
                continue
                
            print(f"\nComando: {command.upper()}")
            print(f"Amostras: {len(samples)}")
            
            if len(samples) > 1:
                # Compara amostras para encontrar bytes fixos e variáveis
                fixed_bytes = []
                variable_bytes = []
                
                min_length = min(len(s) for s in samples)
                for i in range(0, min_length, 2):  # Processa em pares hex
                    byte_values = set()
                    for sample in samples:
                        if i + 1 < len(sample):
                            byte_values.add(sample[i:i+2])
                    
                    if len(byte_values) == 1:
                        fixed_bytes.append((i//2, list(byte_values)[0]))
                    else:
                        variable_bytes.append((i//2, byte_values))
                
                print(f"  Bytes fixos: {fixed_bytes}")
                print(f"  Bytes variáveis: {variable_bytes}")
            else:
                print(f"  Dados: {samples[0] if samples else 'N/A'}")

def main():
    parser = argparse.ArgumentParser(description='Ferramenta de Engenharia Reversa SJRC F11')
    parser.add_argument('--capture', action='store_true', help='Inicia captura de pacotes')
    parser.add_argument('--analyze', type=str, help='Analisa arquivo de pacotes')
    parser.add_argument('--interface', type=str, default='wlan0', help='Interface de rede')
    parser.add_argument('--output', type=str, default='packets.json', help='Arquivo de saída')
    parser.add_argument('--duration', type=int, default=60, help='Duração da captura em segundos')
    
    args = parser.parse_args()
    
    if args.capture:
        print("=== FERRAMENTA DE ENGENHARIA REVERSA SJRC F11 ===")
        print("INSTRUÇÕES:")
        print("1. Certifique-se de que o drone está conectado à sua rede Wi-Fi")
        print("2. Abra o aplicativo móvel oficial")
        print("3. Durante a captura, execute comandos no aplicativo:")
        print("   - Decolar")
        print("   - Mover para frente/trás/lados")
        print("   - Rotacionar")
        print("   - Pousar")
        print("4. Pressione Ctrl+C para parar a captura")
        print()
        
        capture = PacketCapture(args.interface)
        
        try:
            # Inicia captura em thread separada
            capture_thread = threading.Thread(target=capture.start_capture)
            capture_thread.daemon = True
            capture_thread.start()
            
            # Aguarda duração especificada ou interrupção manual
            time.sleep(args.duration)
            
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário")
            
        finally:
            capture.stop_capture()
            capture.save_packets(args.output)
            capture.analyze_patterns()
            
    elif args.analyze:
        print(f"Analisando arquivo: {args.analyze}")
        try:
            with open(args.analyze, 'r') as f:
                packets = json.load(f)
            
            print(f"Carregados {len(packets)} pacotes")
            
            # Análise básica
            analyzer = DroneProtocolAnalyzer()
            
            # Aqui você adicionaria lógica para classificar pacotes por comando
            # baseado em timestamps e padrões conhecidos
            
            analyzer.analyze_command_structure()
            
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {args.analyze}")
        except json.JSONDecodeError:
            print(f"Erro ao ler arquivo JSON: {args.analyze}")
            
    else:
        parser.print_help()
        print("\nEXEMPLOS DE USO:")
        print("  python reverse_engineering_tool.py --capture --duration 120")
        print("  python reverse_engineering_tool.py --analyze packets.json")
        print("\nPARA CAPTURA COMPLETA, USE WIRESHARK:")
        print("  sudo wireshark -i wlan0 -f 'host 192.168.4.1'")

if __name__ == '__main__':
    main()

