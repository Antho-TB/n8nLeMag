# n8n-LeMag

## Description
Dépôt contenant l'infrastructure as-code des automatisations n8n pour l'application "Le Mag" (TB Groupe).
Ce projet gère le flux de publication des actualités soumises via l'Intranet en automatisant le traitement par le modèle d'intelligence artificielle Gemini (Google Cloud) et la génération de brouillons natifs vers WordPress.

## Architecture & Stratégie
Suite à l'optimisation de l'infrastructure, l'architecture repose sur un modèle **Event-Driven (Webhook)**, remplaçant l'ancien système de "Polling SQL".

- **Performance et Fiabilité** : Le déclenchement instantané des requêtes HTTP POST (Webhook) depuis Elementor permet d'éviter l'engorgement de la base de données WordPress.
- **Intégration Modèle IA** : Utilisation du modèle `gemini-1.5-flash-latest` pour garantir rapidité, conformité au niveau des tokens, et stabilité à long terme sans expiration d'API.
- **Surveillance Dédiée** : Un workflow indépendant intercepte les échecs (timeouts, données asynchrones non attendues) et notifie automatiquement l'équipe de développement par email.

## Structure du Dépôt

* `lemag_webhook.json` : Workflow principal de production (Webhook Elementor -> Data Formatting -> LLM `gemini-1.5-flash-latest` -> WordPress).
* `surveillance_erreurs_mail.json` : Workflow de monitoring d'erreur (Error Trigger -> Notification SMTP/Workspace). Attaché en fallback global du workflow principal.
* `lemag_original.json` : Point de restauration historique (Architecture Schedule/SQL obsolète).

## Déploiement

1. Ouvrir l'environnement cible n8n.
2. Importer le workflow d'erreur (`surveillance_erreurs_mail.json`) et configurer les credentials Google/SMTP. Activer le workflow.
3. Importer le workflow principal (`lemag_webhook.json`).
4. Lier le workflow d'erreur dans les **Settings** (Paramètres > Error Workflow) du workflow principal.
5. Activer le workflow principal.
6. Mettre à jour l'URL du noeud Elementor `Action After Submit: Webhook` sur le front-end WordPress.

**Point réseau (Sécurité)** : Assurez-vous que le pare-feu SSRF de WordPress n'entrave pas le trafic sortant vers les sous-réseaux locaux internes (`reject_unsafe_urls = false`), ou que l'instance n8n possède un nom d'hôte validé et approuvé par le FQDN de l'entreprise.
