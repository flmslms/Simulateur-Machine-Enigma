# 🛠️ Enigmachine - Documentation

## ⚙️ 1. Fenêtre de Configuration
La fenêtre de configuration permet de définir les paramètres initiaux de la machine Enigma.

![Fenêtre de Configuration](config_window.png)

- **Choix du réflecteur** : Sélection du type de réflecteur (UKW-B ou UKW-C, les deux seuls implémentés dans ce projet).
- **Choix des rotors** : Sélection des trois rotors utilisés (I, II, III, IV et V).
- **Positions des anneaux** : Définition des positions initiales des anneaux sous la forme:
   - `<ANNEAU ROTOR GAUCHE><ANNEAU ROTOR CENTRE><ANNEAU ROTOR DROIT>` (exemple: `JCB`).
- **Validation des paramètres** : Enregistrement des réglages en cliquant sur le bouton "VALIDER".
- **Annulation des modifications** : Réinitialisation des réglages en cliquant sur le bouton "ANNULER".

## 🖥️ 2. Fenêtre Principale
La fenêtre principale permet d'interagir avec la machine Enigma pour chiffrer et déchiffrer des messages.

![Fenêtre Principale](main_window.png)

- **Paramètres des rotors** : Ajustement de la position des rotors. Vous pouvez cliquer sur la flèche pour décaler d'un cran.
- **Mise à zéro des paramètres** : Réinitialisation des réglages via le bouton "REINITIALISER".
- **Ouverture de la configuration** : Accès aux réglages via "CONFIGURER" (fenêtre configuration vu dans la partie 1).
- **Historique du chiffrement et déchiffrement** : Visualisation des lettres encodées et décodées.
- **Paramètres du câblage** : Configuration des connexions entre les lettres. Ecrivez la lettre associée dans la case en dessous, ou double-cliquez pour l'enlever.
- **Clavier et lampes** : Appuyez sur le clavier numérique, ou sur votre clavier physique et la lettre chiffrée sera illuminée en bleu.

