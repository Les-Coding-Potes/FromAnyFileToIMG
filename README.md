# FromAnyFileToIMG


## Explication

Ce code permet de convertir n'importe quel fichier en image. (il y a forcément une limitation sur la taille du fichier mais elle est assez grande j'ai par exemple testé un fichier à `570 000KB` et ca marchait en generant une image a `137 000KB` )

:warning: Attention pour l'instant le code n'est pas terminé la restoration du fichier d'origine se fait en format texte, a voir comment faire pour reconnaitre quel type de fichier a été passé en entrée. (stocker dans les bytes de fin `nomfichier.monextension` ou enregistrer l'image sous le nom `nomfichier.monextension.png` ou encore utiliser les metadatas de l'image) 

voici un exemple de l'image généré par un fichier text :

![output_image](https://github.com/Les-Coding-Potes/FromAnyFileToIMG/assets/72389130/9dddc5d3-2567-4ebe-bfb7-6b49f2e5475a)![output_image](https://github.com/Les-Coding-Potes/FromAnyFileToIMG/assets/72389130/e0c57239-e7fb-4781-b346-f93e55a16a96)

## Pour aller plus loin

On pourrait imaginer depasser la limite de taille de fichier. Pour se faire on pourrait faire en sorte que si l'image est trop grande on la stock en format gif/video en utilisant des frames d'images.

On pourrait également envisager d'autres format de sorti (Ex : Audio)

L'encodage pourrait être améliorer 
