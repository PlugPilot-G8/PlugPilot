# PlugPilot ⚡

PlugPilot é um sistema de gerenciamento de carregadores para veículos elétricos, desenvolvido com foco em monitoramento, reservas e melhor aproveitamento dos pontos de recarga.

O projeto surgiu da observação de que o problema não está apenas na quantidade de carregadores disponíveis, mas também na forma como eles são utilizados. Muitas vezes um veículo continua ocupando a vaga mesmo após concluir a recarga, reduzindo a disponibilidade para outros motoristas.

Nosso objetivo é tornar o uso desses carregadores mais eficiente tanto para empresas quanto para usuários.

---

## Objetivo

O PlugPilot possui dois públicos principais:

### B2B

Empresas e estabelecimentos que disponibilizam carregadores em seus espaços.

Com o sistema, é possível acompanhar:

* carregadores cadastrados
* reservas realizadas
* status dos carregadores
* informações operacionais básicas

### B2C

Motoristas de veículos elétricos.

Com o sistema, o motorista pode:

* visualizar carregadores disponíveis
* realizar reservas
* cancelar reservas
* acompanhar disponibilidade em tempo real

O diferencial do projeto está na integração com hardware Arduino, permitindo validação física do uso real do carregador.

---

## MVP atual

Atualmente o projeto conta com:

* cadastro e login de usuários
* diferenciação entre motorista e empresário
* CRUD de carregadores
* CRUD de unidades
* sistema de reservas
* dashboard empresarial básico
* persistência de dados em JSON
* integração inicial com Arduino

---

## PlugFlow | Protótipo Arduino

PlugFlow é o módulo de hardware do PlugPilot.

Cada fase do desenvolvimento do protótipo foi realizada em aproximadamente uma semana.

### Fase 1 — Comunicação serial com Python

Primeira versão do Arduino, montada apenas com os componentes necessários para realizar a comunicação serial com o sistema Python.

<img src="./docs/images/fase-1.jpeg" alt="Arduino preparado para comunicação serial com Python" width="500"/>

### Fase 2 — Controle do funcionamento com relé

Integração do módulo relé ao Arduino, permitindo que o sistema controle fisicamente o funcionamento da carga conectada.

<img src="./docs/images/fase-2-rele.jpeg" alt="Arduino controlando o funcionamento de uma carga com relé" width="500"/>

### Fase 3 — LCD e código completo

Versão com tela LCD integrada e código completo, representando o protótipo funcional próximo de sua montagem final.

<img src="./docs/images/fase-3-lcd.jpeg" alt="Arduino com tela LCD e código completo" width="500"/>

### Fase 4 — Protótipo na case de MDF

Versão final do protótipo montada em uma case cortada em MDF, com tela LCD, botão de controle e indicadores luminosos.

<img src="./docs/images/fase-4-case-mdf.jpeg" alt="Versão final do PlugFlow montada em uma case de MDF" width="500"/>

---

## Tecnologias utilizadas

* Python
* JSON
* SQLite *(migração planejada)*
* Arduino
* PySerial
* Matplotlib
* NumPy

---

## Como executar

```bash
git clone https://github.com/PlugPilot-G8/PlugPilot.git
cd PlugPilot
pip install -r requirements.txt
python main.py
```

---

## Equipe

| Nome                                    |
| --------------------------------------- | 
| Antônio Marcos Soares de Araújo Filho   | 
| Carlos Frederico Chaves Gomes Filho     | 
| Guilherme Fonteles Matos da Silva       |
| Lucas Soares Pereira                    | 
| Pedro Henrique Peixoto Campelo          | 
| Pedro Otávio Gomes de Moura Silva       | 
| Victor Bacelar Palazzin                 | 

---
