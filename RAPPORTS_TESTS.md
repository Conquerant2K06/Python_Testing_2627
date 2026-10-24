# Rapport de Tests - Projet GUDLFT

## 1. Contexte
Projet de réservation de places de compétitions (GUDLFT).
Correction des bogues de la Phase 1 et ajout de la fonctionnalité de la Phase 2 (Tableau des points).

## 2. Stratégie de test
- **Tests unitaires** : Validation de la logique métier (dossier `tests/unitaires/`).
- **Tests d'intégration** : Validation des routes et du rendu HTML (dossier `tests/integration/`).
- **Tests de performance** : Locust (6 utilisateurs simultanés).
- **Couverture de code** : Coverage (généré dans `htmlcov/`).
- **Qualité du code** : Flake8 (0 erreur).

## 3. Bogues corrigés (Phase 1)
| Bug | Description | Branche Git |
|---|---|---|
| B1 | Crash sur email inconnu | `bug/email-inconnu` |
| B2 | Crash sur URL invalide | `bug/url-invalide` |
| B3 | Réservation de places négatives | `bug/places-negatives` |
| B4 | Dépassement des places disponibles | `bug/pas-assez-de-places` |
| B5 | Dépassement des points du club | `bug/pas-assez-de-points` |
| B6 | Limite de 12 places dépassée | `bug/limite-12-places` |
| B7 | Points non déduits après réservation | `bug/mise-a-jour-points` |
| B8 | Message d'erreur non affiché | `bug/affichage-messages-erreur` |
| B9 | Compétitions passées réservables | `bug/competitions-passees` |
| B10 | Limite de 12 places non vérifiée en cumulé | `bug/limite-12-cumul` |
| B11 | Bouton retour (Erreur 405) | `bug/bouton-retour` |

## 4. Nouvelles fonctionnalités (Phase 2)
- **Page des points (`/points`)** : Accessible sans connexion, affichant les points de tous les clubs. (Branche : `feature/tableau-des-points`).

## 5. Résultats
- **Tests unitaires** : 5/5 réussis.
- **Tests d'intégration** : 3/3 réussis.
- **Couverture de code** : [Indique ici ton pourcentage, ex: 95%] (voir dossier `htmlcov`).
- **Tests de performance** : 0% d'échec, temps de réponse < 50ms (voir `Rapport_Performance.html`).
- **Flake8** : 0 erreur.