# Guia Rápido - Controlador SJRC F11

## Instalação Rápida

1. **Baixe o projeto** para seu computador
2. **Abra o terminal** na pasta do projeto
3. **Execute os comandos:**
   ```bash
   cd sjrc-f11-controller
   source venv/bin/activate
   python src/main.py
   ```
4. **Abra seu navegador** em: http://localhost:5000

## Uso Básico

### 1. Conectar ao Drone
- Ligue o drone SJRC F11
- Conecte seu computador ao Wi-Fi do drone (rede "SJRC_F11_XXXX")
- Na interface web, clique em "Conectar"

### 2. Controles Disponíveis
- **🚀 Decolar**: Inicia o voo
- **🛬 Pousar**: Pousa o drone
- **⚠️ Emergência**: Para imediatamente (use com cuidado!)

### 3. Movimento
- **Setas**: Frente, trás, esquerda, direita
- **🔼🔽**: Subir e descer
- **Velocidade**: Ajuste com o slider (10-100%)

### 4. Rotação
- **↺ ↻**: Gira o drone
- **Ângulo**: Define quantos graus girar

### 5. Atalhos de Teclado
- **W/S**: Frente/Trás
- **A/D**: Esquerda/Direita  
- **Q/E**: Subir/Descer
- **R/T**: Girar direita/esquerda
- **ESPAÇO**: Emergência

## ⚠️ IMPORTANTE

- **SEMPRE** mantenha o drone à vista
- **MONITORE** o nível da bateria
- **USE** em área aberta e segura
- **RESPEITE** as leis locais sobre drones

## Problemas Comuns

**Não conecta?**
- Verifique se está na rede Wi-Fi do drone
- Tente o IP: 192.168.4.1

**Comandos não funcionam?**
- O protocolo precisa ser decifrado primeiro
- Use a ferramenta de engenharia reversa incluída

**Para mais detalhes, consulte o README.md completo**

