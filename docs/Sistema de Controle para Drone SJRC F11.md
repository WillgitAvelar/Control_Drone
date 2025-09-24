# Sistema de Controle para Drone SJRC F11

**Desenvolvido por:** Manus AI  
**Data:** Setembro 2025  
**Versão:** 1.0

## Visão Geral

Este projeto apresenta uma solução completa para controlar o drone SJRC F11 através de um computador, substituindo o controle remoto físico por uma interface web moderna e intuitiva. O sistema foi desenvolvido em resposta à necessidade de criar uma alternativa de controle quando o joystick original não está disponível.

O drone SJRC F11 é um quadricóptero GPS com câmera 4K que utiliza comunicação Wi-Fi para transmissão de vídeo e controle via aplicativo móvel. Este projeto explora a engenharia reversa do protocolo de comunicação proprietário para possibilitar o controle direto via computador.

## Características do Sistema

### Interface Web Responsiva
O sistema apresenta uma interface web moderna e intuitiva que funciona em qualquer navegador, oferecendo controle completo do drone através de botões visuais e atalhos de teclado. A interface é totalmente responsiva, adaptando-se a diferentes tamanhos de tela, desde desktops até tablets.

### Controles Disponíveis
- **Controles Básicos:** Decolagem, pouso e parada de emergência
- **Movimento Direcional:** Frente, trás, esquerda, direita, subir e descer
- **Rotação:** Rotação horária e anti-horária com controle de ângulo
- **Controle de Velocidade:** Slider ajustável de 10% a 100%
- **Atalhos de Teclado:** Controle via WASD, QE para altitude, RT para rotação

### Monitoramento em Tempo Real
O sistema exibe informações de status do drone em tempo real, incluindo:
- Nível da bateria
- Altitude atual
- Velocidade de voo
- Sinal GPS (número de satélites)
- Status de conexão

### Log de Atividades
Todas as ações e comandos são registrados em um log visual com timestamps, facilitando o monitoramento e depuração de problemas.

## Arquitetura Técnica

### Backend Flask
O backend é desenvolvido em Python usando o framework Flask, fornecendo uma API RESTful para comunicação com o drone. A arquitetura modular permite fácil extensão e manutenção do código.

### Comunicação de Rede
O sistema utiliza sockets UDP para comunicação direta com o drone através da rede Wi-Fi. O protocolo de comunicação é baseado em engenharia reversa do tráfego entre o aplicativo móvel oficial e o drone.

### Frontend Responsivo
A interface web é desenvolvida em HTML5, CSS3 e JavaScript vanilla, sem dependências externas, garantindo compatibilidade máxima e carregamento rápido.

## Limitações e Considerações

### Protocolo Proprietário
O maior desafio deste projeto é o protocolo de comunicação proprietário do SJRC F11. Sem documentação oficial, é necessário realizar engenharia reversa do tráfego de rede para decifrar os comandos de controle.

### Processo de Engenharia Reversa
A implementação atual fornece uma estrutura base para o controle, mas os comandos específicos precisam ser descobertos através de análise de pacotes de rede. O sistema inclui ferramentas para facilitar este processo.

### Segurança e Responsabilidade
O controle de drones apresenta riscos inerentes. Este sistema deve ser usado apenas por operadores experientes e em ambientes seguros. Sempre mantenha o drone dentro do alcance visual e respeite as regulamentações locais.

## Estrutura do Projeto

```
sjrc-f11-controller/
├── src/
│   ├── main.py                 # Aplicação Flask principal
│   ├── routes/
│   │   ├── drone_control.py    # API de controle do drone
│   │   └── user.py            # Rotas de usuário (template)
│   ├── models/
│   │   └── user.py            # Modelos de dados
│   ├── static/
│   │   └── index.html         # Interface web
│   └── database/
│       └── app.db             # Banco de dados SQLite
├── reverse_engineering_tool.py # Ferramenta de engenharia reversa
├── requirements.txt            # Dependências Python
└── README.md                  # Esta documentação
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.7 ou superior
- Drone SJRC F11 funcional
- Rede Wi-Fi para comunicação com o drone
- Navegador web moderno

### Instalação
1. Clone ou baixe o projeto para seu computador
2. Navegue até o diretório do projeto
3. Ative o ambiente virtual: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute a aplicação: `python src/main.py`
6. Acesse http://localhost:5000 no seu navegador

### Configuração da Rede
1. Ligue o drone SJRC F11
2. Conecte seu computador à rede Wi-Fi do drone (geralmente "SJRC_F11_XXXX")
3. Configure o IP do drone na interface (padrão: 192.168.4.1)
4. Clique em "Conectar" para estabelecer comunicação

## Uso do Sistema

### Conexão Inicial
Após iniciar a aplicação, acesse a interface web e configure o IP do drone. O IP padrão (192.168.4.1) funciona na maioria dos casos, mas pode variar dependendo da configuração específica do seu drone.

### Controles Básicos
Use os botões "Decolar" e "Pousar" para controles básicos de voo. O botão de "Parada de Emergência" deve ser usado apenas em situações críticas, pois pode causar queda abrupta do drone.

### Movimento e Navegação
Os controles de movimento permitem navegação precisa em todas as direções. Ajuste a velocidade usando o slider antes de enviar comandos de movimento. Os atalhos de teclado oferecem controle mais rápido para usuários experientes.

### Monitoramento
Acompanhe constantemente o status do drone, especialmente o nível da bateria. Pouse o drone imediatamente quando a bateria estiver baixa para evitar acidentes.

## Engenharia Reversa do Protocolo

### Ferramenta Incluída
O projeto inclui uma ferramenta especializada (`reverse_engineering_tool.py`) para capturar e analisar o tráfego de rede entre o aplicativo móvel oficial e o drone.

### Processo Recomendado
1. Configure seu computador como ponto de acesso Wi-Fi
2. Conecte tanto o drone quanto o dispositivo móvel ao seu hotspot
3. Use Wireshark ou a ferramenta incluída para capturar pacotes
4. Execute comandos no aplicativo móvel oficial
5. Analise os pacotes para identificar padrões de comando

### Análise de Pacotes
A ferramenta de engenharia reversa pode identificar:
- Padrões de bytes fixos e variáveis em comandos
- Estrutura de pacotes por tipo de comando
- Frequência e timing de comunicação
- Checksums e validação de dados

## Solução de Problemas

### Problemas de Conexão
Se não conseguir conectar ao drone:
- Verifique se está conectado à rede Wi-Fi do drone
- Confirme o IP correto do drone
- Reinicie o drone e tente novamente
- Verifique se não há interferência de outras redes Wi-Fi

### Comandos Não Respondem
Se os comandos não surtem efeito:
- Verifique se o protocolo foi corretamente decifrado
- Confirme se o drone está em modo de voo
- Verifique a distância e qualidade do sinal Wi-Fi
- Consulte o log de atividades para mensagens de erro

### Performance
Para melhor performance:
- Use uma conexão Wi-Fi estável e próxima
- Evite interferências de outros dispositivos
- Mantenha o sistema atualizado
- Monitore o uso de recursos do computador

## Desenvolvimento Futuro

### Melhorias Planejadas
- Implementação completa do protocolo decifrado
- Suporte a múltiplos modelos de drone SJRC
- Interface de programação de voos autônomos
- Integração com sistemas de telemetria avançados
- Suporte a controles de gamepad/joystick USB

### Contribuições
Este projeto é open source e aceita contribuições da comunidade. Áreas prioritárias incluem:
- Decifração completa do protocolo SJRC F11
- Testes com diferentes versões do firmware
- Melhorias na interface do usuário
- Documentação adicional

## Considerações Legais e de Segurança

### Responsabilidade do Usuário
O uso deste sistema é de inteira responsabilidade do usuário. O desenvolvedor não se responsabiliza por acidentes, danos ou uso inadequado do sistema.

### Regulamentações
Sempre respeite as regulamentações locais sobre uso de drones, incluindo:
- Registro do equipamento quando necessário
- Restrições de altitude e área de voo
- Distância de aeroportos e zonas proibidas
- Privacidade e direitos de terceiros

### Segurança Operacional
- Nunca voe o drone fora do alcance visual
- Mantenha sempre uma rota de pouso de emergência disponível
- Monitore constantemente o nível da bateria
- Evite voos em condições climáticas adversas
- Mantenha distância segura de pessoas e propriedades

## Suporte e Comunidade

### Documentação
Esta documentação será continuamente atualizada conforme o projeto evolui. Consulte regularmente para obter as informações mais recentes.

### Relatório de Problemas
Para reportar bugs ou solicitar recursos, utilize os canais apropriados do projeto. Inclua sempre:
- Versão do sistema operacional
- Modelo específico do drone
- Logs de erro detalhados
- Passos para reproduzir o problema

### Comunidade de Desenvolvedores
Junte-se à comunidade de desenvolvedores interessados em projetos de drone open source. Compartilhe experiências, soluções e contribua para o desenvolvimento coletivo.

---

**Aviso:** Este projeto é experimental e destinado a fins educacionais e de pesquisa. Use por sua própria conta e risco. Sempre priorize a segurança e siga as melhores práticas de operação de drones.

