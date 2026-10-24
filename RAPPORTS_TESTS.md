# Rapport de Tests - Projet GUDLFT

## 1. Contexte
Projet de réservation de places de compétitions (GUDLFT).
Correction des bogues de la Phase 1 et ajout de la fonctionnalité de la Phase 2 (Tableau des points).

## 2. Stratégie de test
- **Tests unitaires** : Validation de la logique métier (dossier `tests/unitaires/`).
- **Tests d'intégration** : Validation des routes et du rendu HTML (dossier `tests/integration/`).
- **Tests de performance** : Locust (6 utilisateurs simultanés).
- **Couverture de code** : Coverage.
- **Qualité du code** : Flake8 (0 erreur).

## 3. Bogues corrigés (Phase 1)
| Bug | Description | Branche Git |
|---|---|---|
| B1 | Crash sur email inconnu | `bugfix/unknown-email-crash` |
| B2 | Crash sur URL invalide | `bugfix/invalid-url-crash` |
| B3 | Réservation de places négatives | `bugfix/negative-places` |
| B4 | Dépassement des places disponibles | `bugfix/not-enough-places` |
| B5 | Dépassement des points du club | `bugfix/not-enough-points` |
| B6 | Limite de 12 places dépassée | `bugfix/max-12-places` |
| B7 | Points non déduits après réservation | `bugfix/update-club-points` |
| B8 | Message d'erreur non affiché | `bugfix/flash-messages-display` |
| B9 | Compétitions passées réservables | `bugfix/past-competitions` |
| B10 | Limite de 12 places non vérifiée en cumulé | `bugfix/max-12-cumulative` |
| B11 | Bouton retour (Erreur 405) | `bugfix/fix-back-button` |

## 4. Nouvelles fonctionnalités (Phase 2)
- **Page des points (`/points`)** : Accessible sans connexion, affichant les points de tous les clubs (conformément aux spécifications).

## 5. Résultats
- **Tests unitaires** : 5/5 réussis.
- **Tests d'intégration** : 3/3 réussis.
- **Couverture de code** : > 90% (voir dossier `htmlcov`).
- **Tests de performance** : 0% d'échec (voir `Rapport_Performance.html`).
- **Flake8** : 0 erreur.