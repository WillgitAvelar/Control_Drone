
## Pesquisa Inicial - SJRC F11

**Pontos Chave:**

*   O drone SJRC F11 (e suas variantes como 4K Pro) utiliza Wi-Fi para FPV e controle via aplicativo móvel.
*   Não há documentação oficial ou pública sobre o protocolo de comunicação específico para controle via computador.
*   A maioria dos resultados de busca aponta para manuais de usuário, vídeos de unboxing/review e problemas comuns, não para detalhes técnicos de comunicação.
*   A ideia de "reverse engineering" do protocolo de comunicação é mencionada em contextos gerais de drones, mas não especificamente para o SJRC F11 em uma solução pronta.
*   Ferramentas como Wireshark são sugeridas para análise de pacotes em processos de engenharia reversa de protocolos de drones.
*   Bibliotecas como `Dronekit Python` são mencionadas para controle de drones, mas geralmente para plataformas mais abertas como Pixhawk, não para drones de consumo com protocolos proprietários.

**Próximos Passos:**

1.  Investigar mais a fundo a comunicação Wi-Fi do SJRC F11: qual banda (2.4GHz/5GHz), tipo de rede (Ad-hoc/Access Point), e se há alguma informação sobre a estrutura dos pacotes.
2.  Procurar por projetos de engenharia reversa de drones de consumo similares ao SJRC F11 que possam ter documentação ou código-fonte disponível.
3.  Explorar a viabilidade de usar ferramentas de análise de rede (como Wireshark) para capturar e analisar o tráfego entre o aplicativo móvel e o drone, a fim de inferir o protocolo de controle.
4.  Avaliar se é possível emular o comportamento do aplicativo móvel para enviar comandos ao drone.



## Análise de Opções de Comunicação e Controle

**Viabilidade da Engenharia Reversa:**

A engenharia reversa do protocolo Wi-Fi do SJRC F11 é a abordagem mais provável para controlar o drone via computador, dada a ausência de documentação oficial. Isso envolverá a captura e análise do tráfego de rede entre o drone e o aplicativo móvel oficial.

**Ferramentas e Métodos para Engenharia Reversa:**

*   **Wireshark:** Uma ferramenta essencial para a captura e análise de pacotes de rede. Será necessário configurar um ponto de acesso Wi-Fi ou usar um adaptador Wi-Fi em modo monitor para capturar o tráfego entre o drone e o dispositivo móvel [2, 3, 4, 5].
*   **Análise de Tráfego:** Identificar padrões nos pacotes de dados que correspondem a comandos específicos (decolar, pousar, mover para frente/trás/lados, etc.) e telemetria (posição, bateria, etc.). Isso pode envolver a variação de comandos no aplicativo e a observação das mudanças no tráfego de rede.
*   **Linguagens de Programação:** Python é uma escolha popular para o desenvolvimento de scripts de controle de drones, especialmente com bibliotecas que podem interagir com sockets de rede para enviar e receber dados [11, 12, 13, 14].

**Desafios Potenciais:**

*   **Criptografia:** O tráfego pode ser criptografado, o que dificultaria a análise e a replicação dos comandos. No entanto, muitos drones de consumo usam criptografia mínima ou nenhuma para o tráfego de controle.
*   **Protocolo Proprietário:** O protocolo será proprietário e não documentado, exigindo um esforço significativo para decifrar a estrutura dos pacotes e a lógica de comunicação.
*   **Estabilidade da Conexão:** A conexão Wi-Fi do drone pode ser sensível a interferências, afetando a confiabilidade do controle.
*   **Segurança:** A manipulação de drones sem o controle original pode apresentar riscos de segurança e perda do equipamento.

**Alternativas (menos prováveis para este drone):**

*   **Bibliotecas de Controle de Drones:** `Dronekit` e outras bibliotecas Python são excelentes para drones de código aberto (como os baseados em Pixhawk ou ArduPilot), mas improváveis de funcionar diretamente com o SJRC F11 devido ao seu protocolo proprietário.
*   **Módulos de Rádio:** A substituição do módulo de rádio do drone por um compatível com protocolos abertos (como o que é usado em rádios de hobby) exigiria modificações de hardware e firmware, o que está além do escopo de um controle via software.

**Conclusão da Análise:**

A engenharia reversa do protocolo Wi-Fi é a única abordagem viável para criar um sistema de controle baseado em computador para o SJRC F11. Isso exigirá tempo e conhecimento técnico em análise de rede e programação. O processo envolverá a captura de pacotes, análise de dados e, em seguida, a implementação de um cliente que possa enviar os comandos decifrados.

**Referências:**

[1] https://manuals.plus/sjrc/f11-4k-pro-folding-aircraft-manual
[2] https://hackernoon.com/how-to-reverse-engineer-a-drone-with-wireshark-using-packet-dissection
[3] https://www.digidow.eu/publications/2021-christof-masterthesis/Christof_2021_MasterThesis_DJIProtocolReverseEngineering.pdf
[4] https://mavicpilots.com/threads/low-level-wifi-protocol-reverse-engineering.111099/
[5] https://medium.com/@cyberengage.org/master-wireshark-tool-like-a-pro-the-ultimate-packet-analysis-guide-for-real-world-analysts-981fb9024e7d
[6] https://www.wireshark.org/docs/wsug_html/
[7] https://www.youtube.com/watch?v=n4muxtqLhN4
[8] https://labex.io/tutorials/wireshark-how-to-analyze-packet-data-in-wireshark-for-cybersecurity-investigations-415160
[9] https://quadcopterforum.com/threads/cannot-get-f11-4k-pro-drone-camera-to-video-feed-phone-app.25965/
[10] https://apps.apple.com/us/app/sj-f-pro/id1509631290
[11] https://dojofordrones.com/drone-programming/
[12] https://www.thedronegirl.com/2025/07/28/program-drone-python/
[13] https://www.reddit.com/r/diydrones/comments/14s108/controlling_pixhawk_drone_with_python/
[14] https://www.youtube.com/watch?v=lgqBFj1rkbw

