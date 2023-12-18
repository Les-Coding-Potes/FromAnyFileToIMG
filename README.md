# FromAnyFileToIMG


## Explication

Ce code permet de convertir n'importe quel fichier en image. (il y a forcément une limitation sur la taille du fichier mais elle est assez grande j'ai par exemple testé un fichier à `570 000KB` et ca marchait en generant une image a `137 000KB` )

voici un exemple de l'image généré par un fichier text :

![output_image](https://github.com/Les-Coding-Potes/FromAnyFileToIMG/assets/72389130/9dddc5d3-2567-4ebe-bfb7-6b49f2e5475a)![output_image](https://github.com/Les-Coding-Potes/FromAnyFileToIMG/assets/72389130/e0c57239-e7fb-4781-b346-f93e55a16a96)


Le fichier qui est envoyé en entrée est converti en image son extension est alors modifiée passant de `nomfichier.monextension` à `nomfichier.monextension.png`

## Mettre le code sur un raspberry

Exemple de connexion via ssh au raspberry :

```bash
ssh 192.168.63.209 -l exarilo
```

Deplacez vous dans le dossier qui contiendra le code et coller le code dans chacun des fichiers :

:warning: il vous faudra modifier légérement le fichier api.py en remplacer les occurences de "/home/exarilo/Documents/" par le chemin du dossier qui va contenir les fichiers (`pwd` pou obtenir le chemin courant dans un terminal linux)
```bash
sudo nano api.py
sudo nano encoder.py
sudo nano decoder.py
```
une fois le code sur le raspberry pi il vous faudra lancer l'api rest : 
```bash
python api.py
```
Si vous voulez ne plus avoir besoin d'executer la commande précedente il vous suffit d'editer un fichier en faisant:
```bash
crontab -e
```
ajoutez a la fin du ficher :
`@reboot python /home/exarilo/Documents/api.py` (remplacez par votre chemin)


