# 🤖 Infrastructure n8n - Le Mag (TB Groupe)

Ce dépôt centralise l'infrastructure as-code des automatisations **n8n** gérant "Le Mag". 
L'objectif de cette architecture est de réceptionner les actualités soumises via le formulaire d'Intranet, de les faire traiter par des modèles d'intelligence artificielle (Google Gemini), puis de les republier automatiquement en tant que Brouillons sur WordPress.

## 🏗️ Architecture

Le système a été migré d'une architecture dite "Polling SQL" (qui interrogeait manuellement la base de données WordPress) vers une **Architecture pure Event-Driven (Webhook)**. 

### Avantages :
1. **Temps réel** : L'IA se déclenche à la milliseconde près suite à la validation dans Elementor.
2. **Allégement Base de Données** : Suppression des boucles de surveillance incessantes sur MySQL.
3. **Robustesse et Scaling** : Utilisation du modèle `gemini-1.5-flash-latest` capable de gérer des requêtes parallèles rapides sans expiration.

---

## 🗂️ Fichiers du dépôt

* `lemag_webhook.json` : **(Production Actuelle)** Le workflow principal événementiel. Déclenché par un Webhook Elementor, formate les données, génère l'article via Gemini, et poste sur WordPress.
* `surveillance_erreurs_mail.json` : Le workflow de **monitoring et d'alerte**. Ce module est directement greffé au workflow principal et expédie un email d'alerte avec un lien de diagnostic automatique en cas de défaillance (perte de connexion, timeout de l'IA, type inattendu).
* `lemag_original.json` : **(Archive)** L'ancien workflow basé sur le déclencheur Schedule/SQL pour documentation et historique.

---

## ⚙️ Installation / Import

Si vous devez reconstruire l'infrastructure sur un nouveau serveur n8n :

1. Naviguez dans l'interface de n8n.
2. Allez dans *Workflows* > *Import from File* et importez `surveillance_erreurs_mail.json`. Configurez immédiatement les "Credentials" Google/SMTP.
3. Activez le workflow de surveillance.
4. Importez ensuite `lemag_webhook.json`.
5. Dans les paramètres globaux (Settings) de `LeMag_Webhook`, attribuez-lui le workflow de surveillance dans la rubrique **Error Workflow**.
6. Branchez la nouvelle URL issue du nœud Webhook dans le module **Action After Submit** de votre formulaire Elementor sur WordPress.

*(N.B : Assurez-vous d'avoir désactivé la protection SSRF sur le WordPress émetteur si n8n se trouve sur le même réseau local).*
