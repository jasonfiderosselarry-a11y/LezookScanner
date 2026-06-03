# ╔══════════════════════════════════════════════════════════╗
# LEZOOK SCANNER v3.0
# OSINT + Vulnerability Detection Framework
# Contact : +261 32 542 10
# Email : jason.fiderosse.larry@gmail.com
# ╚══════════════════════════════════════════════════════════╝
 ## ⚠️ AVERTISSEMENT LÉGAL / LEGAL WARNING
Cet outil est EXCLUSIVEMENT destiné à :
- Les programmes Bug Bounty autorisés (HackerOne, Bugcrowd, Intigriti,
YesWeHack...)
- Les tests de pénétration sur des systèmes dont vous êtes propriétaire ou pour
lesquels vous avez une autorisation écrite
- La recherche en sécurité éthique et à des fins éducatives
 NE JAMAIS utiliser sur des cibles sans autorisation explicite écrite.
 ---
 ## 🔧 INSTALLATION RAPIDE
 ### 1. Prérequis
- Python 3.8 ou supérieur
 ### 2. Installer les dépendances
 # Méthode recommandée
pip install kivymd kivy
 # Si erreur sur Linux (Ubuntu/Debian), installer d'abord :
sudo apt-get install python3-pip python3-dev \
libgl1-mesa-dev libgles2-mesa-dev \
libsdl2-dev libsdl2-image-dev \
libsdl2-mixer-dev libsdl2-ttf-dev
 # Sur Windows / macOS :
pip install kivymd kivy
 ### 3. Lancer l'outil
 python main.py
---
 ## 🧩 MODULES OSINT
 | Module | Description |
|---------------------|-------------------------------------------------------|
| DNS Resolution | Résolution domaine → adresses IP |
| Reverse DNS | IP → nom d'hôte (PTR record) |
| WHOIS Lookup | Registrar, dates, contacts du domaine |
| SSL Certificate | Détails cert, SANs, validité |
| HTTP Headers | Fingerprinting serveur complet |
| DNS Records (dig) | A, AAAA, MX, NS, TXT, CNAME, SOA |
| Subdomain Discovery | 35+ sous-domaines via bruteforce DNS passif |
| GeoIP Location | Pays, ville, ISP, ASN (ip-api.com) |
| Robots / Sitemap | robots.txt, sitemap.xml, chemins cachés |
 ---
 ## ⚡ MODULES VULNÉRABILITÉS (style nmap NSE)
 | Module | Description |
|-------------------------|----------------------------------------------------|
| Port Scan (22 ports) | FTP, SSH, Telnet, SMB, MySQL, RDP, Redis... |
| Banner Grab / Version | Détection versions logicielles obsolètes |
| Security Headers | CSP, HSTS, X-Frame-Options, etc. |
| SSL/TLS Weakness | Proto faibles, cert expiré, TLSv1.0 |
| Sensitive Paths | .env, .git, phpMyAdmin, admin panels... |
| CORS Misconfiguration | Origins wildcard, credentials + CORS ouvert |
| Open Redirect | Paramètres URL redirect vers domaine externe |
 ---
 ## 🎯 INTERFACE
 3 PANNEAUX :
- [ CONSOLE ] → Sortie complète en temps réel
- [ FINDINGS ] → Vulnérabilités triées par sévérité (CRITICAL/HIGH/MEDIUM/LOW)
- [ TARGET INFO ] → Informations consolidées sur la cible
 BOUTONS D'ACTION :
- ▶ SCAN ALL → Lance tous les modules sélectionnés
- ⚡ VULN ONLY → Scan de vulnérabilités uniquement- 🔍 OSINT ONLY → Reconnaissance passive uniquement
- 💾 SAVE REPORT → Export rapport .txt
- 📋 COPY FINDINGS → Copie les findings dans le presse-papiers
 ---
 ## 💡 CONSEILS BUG BOUNTY
 1. EASY WINS (P4/P3) :
- Headers de sécurité manquants (CSP, HSTS, X-Frame-Options)
- Informations de version dans les headers (Server:, X-Powered-By:)
- Fichier robots.txt révélant des chemins sensibles
 2. MEDIUM (P3/P2) :
- CORS mal configuré
- TLS 1.0/1.1 accepté
- Fichier .env ou .git accessible
 3. HIGH/CRITICAL (P2/P1) :
- Redis/MongoDB/Elasticsearch exposés sans auth
- Docker API sur port 2375 exposé
- Certificat invalide/auto-signé
- phpMyAdmin accessible publiquement
 ---
 ## 📞 CONTACT
- Téléphone : +261 32 542 10
- Email : jason.fiderosse.larry@gmail.com
