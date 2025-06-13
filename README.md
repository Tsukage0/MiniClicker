# MiniClicker

https://github.com/Tsukage0/clicker

# v1.1

## Ajout

- Boutton `Change Log` (c'est le même que sur github)
- Boutton `Réinitialiser`


## Modification

- Le fichier `.json` n'ai plus présent dans le dossier avec le `.exe`, il sera dans le dossier `C:\Users\<USER>\AppData\Roaming\MiniClicker`, sous le nom `save.dat` et il est aussi encrypter en base 64, ce n'est pas grand-chose, mais c'est pour une expérience juste :)
- Le calcul derrière la vitesse a été changé (je me suis trompé sur le calcul du coup, ça allait beaucoup trop vite.) et maintenant le max, c'est `+650%` et cela bloque l'amélioration.
- Nom shop : `Acheter Auto-Clicker` -> `Auto-Clicker`
- Les nombres sont maintenant en groupe de 3 (ex : 1 000 000)

L'augmentation des prix dans le shop :
- Auto-Clicker : augmentation du prix de `5%` -> `10%` à chaque amélioration.
- Réduction du Temps : augmentation du prix de `10%` -> `20%` à chaque amélioration.
- Plus de click : augmentation du prix de `20%` -> `50%` à chaque amélioration.


## Bug connue

- Quand vous faite un reset, le shop ne se met pas à jour. Il suffit juste de le fermer et de le réouvrir.

# v1.0

Premier version de l'app, c'est juste un clicker assez simple, mais c'est un petit projet que j'avais envie de faire avec python et pyinstaller

## Présentation

C'est une petite fenêttre où il y a : 
- Le score gagner depuis le debut
- Score par seconde (sps)
- Le boutton principal pour gagner les points
- Un bouton "shop" qui ouvre une autre fenêtre à droite ou à gauche en fonction de la place

Seulement 3 amélioration (pour l'instant) :
- Auto-clicker : 1 point tout les 5 secondes
- Réduction du Temps : Diminue de 10% la duré entre les clicks des auto-clicker (niveau max théorique 130%, car après ça il n'y a plus aucun changement)
- Plus de click : ajoute 1 point a chaque auto-clicker

## Installation

Il y a juste a extraire le zip et laisser le `.exe` dans le dossier.
Pour le `.json` (s'il est présent), cela sert de sauvegarde, pas très pratique, mais ça sert, s'il est supprimé ou que des paramètre sont supprimer, ne vous en faite, ils seront créés automatiquement.

S'il y a le moindre problème n'hésiter pas à me le faire savoir.

Note de fin :
Normalement, j'ai réglé le problème de Windows qui considère le `.exe` comme un virus, du moins avec les testes effectuer de mon côté. Mais si vous avez d'autre anti-virus je ne peut rien promettre.
Tout ce que je peux promettre, c'est qu'il ne fait rien de mal (je suis d'accord, ça sonne mal, mais j'y peux rien.), c'est à cause de pyinstaller, je n'ai pas tout bien compris pourquoi malheureusement.
