Aquest projecte presenta la nostra implementació per als emmagatematges distribuits: centralitzat i descentralitzat. Em enfocat la pràctica en les definicions base d'un sistema centralitzat (slaves connectats a un master que controla) i descentralitzat (els algoritmes controlen els nodes).

El nostre projecte esta format per 2 carpetes importants i més arxius que configuren la nostra implementació:
- Carpeta eval: conté el joc de tests (eval.py + tests), el decentralized.py i la seva configuració (decentralized_config.yaml)
- Carpeta proto: conté el proto que defineix el nostres serveis RPC
- Resta arxius: conté arxius resultants de les proves (backup.txt), el centralized.py, la seva configuraciño (centralized_config.yaml) i un arxiu de prova del servidor que no ens afectarà a la pràctica.

Per a executar el codi només haurem de entrar a la carpeta eval i executar eval.py. En cas de que hi hagi problemes d'execució amb "python3" es pot canviar a "python".