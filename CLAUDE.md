# Instructions Spécifiques au Projet n8nLeMag (TB Groupe)

## Rôle et Contexte
L'IA intervient en tant que Lead Data/AI Engineer assistant le projet.
Le but est d'automatiser et maintenir l'infrastructure n8n.
Ce projet s'inscrit dans un cadre professionnel de production.

## Standards de Codage et de Structure
- **Sobriété** : Pas d'émojis, pas de commentaires superflus ou de métadonnées "Généré par IA". Les réponses et la documentation doivent être rigoureusement factuelles, synthétiques et professionnelles.
- **Langue** : La documentation et les commentaires de code doivent être rédigés en Français (standard professionnel structuré), de manière à être compréhensibles par des développeurs juniors.
- **Architecture** : Les workflows privilégient les déclencheurs (triggers) Event-Driven (Webhooks) par rapport au polling. La redondance logicielle doit être évitée.
- **Transparence** : Toujours documenter avec précision les nœuds de configuration JSON critiques (Timeout, modèle IA, Bypass SSRF).
- **Propreté du Dépôt** : Tous les scripts temporaires (ex: scripts `.js` d'exécution d'API n8n) utilisés pour pousser des mises à jour ou formater des données localement doivent être nettoyés avant chaque commit.

## Résolution d'Incidents
Lors du débogage ou de la création de workflows :
- Toujours adjoindre un "Error Workflow" dédié aux workflows liés à la production pour intercepter les pannes liées au Machine Learning (modèles Gemini API) ou au Réseau.
- Documenter le protocole de déploiement et l'architecture logicielle sans jargon marketing.
