L'exercice demande de répartir 90 élèves (numérotés de 1 à 90)
dans 3 classes en optimisant le critère suivant: chaque élève
a désigné 4 de ses camarades (ordonnés), et si cet élève
retrouve dans sa classe son camarade numéro 1 (resp. 2, 3, 4)
on attribue à l'arrangement 20 points (resp. 15, 10, 5).

Voir le fichier [dghack2021-ecole-repartition.json](dghack2021-ecole-repartition.json).

Le but est de trouver un arrangement donnant au moins 2950 points.

On peut commencer par un algorithme glouton: on répartit les élèves
en 3 classes de taille égale:

```go
for i := range s.classe {
    s.classe[i] = uint32(i % 3)
}
```

ce qui donne un score initial de 1645.

Puis on applique des transpositions en retenant celles qui augmentent
le score:

```go
for k := 0; k < 1e6; k++ {
    i := k % 90
    j := k % 89
    a, b := i, j
    if j >= i {
        b++
    }
    n := s.score
    s.swap(a, b)
    s.score = s.compute()
    n2 := s.score
    if n2 >= n {
        if n2 > n {
            fmt.Println("new score", n2)
        }
    } else {
        s.swap(a, b)
        s.score = n
    }
```

ce qui permet d'atteindre le score honorable de 2870 (qui n'est pas assez).

On peut alors utiliser une approche (librement) inspirée du recuit simulé
pour surmonter cet optimum local et aller un peu plus haut, en tolérant
une transposition qui réduit le score.

On obtient une solution quasiment immédiatement (score=3015):
```
[
  [2,4,8,12,14,16,20,22,23,29,32,33,34,36,38,41,50,53,54,60,64,66,67,70,73,80,83,84,87,90],
  [3,7,9,15,17,19,21,30,31,37,39,40,43,44,46,51,52,55,57,62,68,71,72,74,78,79,81,82,85,86],
  [1,5,6,10,11,13,18,24,25,26,27,28,35,42,45,47,48,49,56,58,59,61,63,65,69,75,76,77,88,89]
]
```

Programme complet: [ecolesolver.go](ecolesolver.go)
