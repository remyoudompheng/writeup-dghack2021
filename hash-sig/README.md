Le but du challenge est de s'authentifier auprès d'un petit
serveur TCP qui demande une signature en réponse à un challenge
(modules fournis [hash_based.py](hash_based.py) et
[client_lib.py](client_lib.py)).

On peut résumer le protocole de cette manière:

* le serveur envoie un message `m`
* on calcule `sha256(m)` composé de 64 chiffres hexadécimaux H
* on extrait une séquence de 34 entiers 8 bits `H[0:2] ... H[31:33], H[0:2], H[1:3]`
* le client doit disposer de 34 clés secrètes sk[i] de 32 octets
* le client calcule `sha256^seq[i](sk[i])` (on applique la fonction
  sha256 `seq[i]` fois sur `sk[i]`).
* le client envoie la concaténation de ces hashs au serveur

Les clés secrètes ne sont pas connus mais une capture Wireshark
est fournie contenant 5 échanges.

Or, si on connaît la valeur de `sha256^A(sk[i])` il suffit d'appliquer
un sha256 pour retrouver `sha256^(A+1)(sk[i])` et ainsi de suite.

La capture réseau fournie correspond à ces 5 séquences `(seq[i])`
```python
from hashlib import sha256
from hash_based import _sequence

for c in challenges:
    digest = sha256(bytes.fromhex(c)).hexdigest()
    seq    = _sequence(digest)
    print(seq)

[21, 93, 208, 1, 17, 26, 175, 249, 145, 24, 130, 41, 158, 226, 32, 15, 250, 172, 206, 237, 209, 23, 126, 238, 224, 6, 106, 169, 144, 10, 170, 166, 21, 93]
[123, 179, 54, 96, 7, 123, 182, 108, 203, 186, 165, 80, 2, 40, 141, 217, 159, 252, 200, 142, 232, 135, 116, 69, 95, 248, 128, 8, 136, 135, 120, 143, 123, 179]
[201, 146, 36, 72, 142, 237, 211, 55, 117, 94, 229, 80, 6, 102, 111, 250, 163, 55, 116, 74, 161, 16, 12, 205, 219, 186, 167, 113, 23, 125, 211, 49, 201, 146]
[91, 184, 132, 68, 77, 221, 214, 99, 51, 53, 88, 129, 19, 59, 187, 182, 107, 180, 70, 107, 190, 224, 2, 38, 111, 240, 5, 81, 29, 221, 220, 200, 91, 184]
[244, 73, 149, 90, 169, 148, 71, 113, 30, 230, 107, 183, 116, 65, 28, 201, 150, 107, 186, 162, 43, 189, 221, 217, 151, 126, 238, 228, 67, 55, 117, 88, 244, 73]
```

On connaît donc déjà les hashs des clés secrètes pour les exposants
suivants:
```python
>>> print([min(x) for x in zip(*seqs)])
[21, 73, 36, 1, 7, 26, 71, 55, 30, 24, 88, 41, 2, 40, 28, 15, 107, 55, 70, 74, 43, 16, 2, 38, 95, 6, 5, 8, 23, 10, 117, 49, 21, 73]
```

Comme ceux-ci sont petits, il suffit d'avoir "de la chance" pour que le
serveur demande un challenge avec une séquence où chaque nombre est plus
grand, et il suffit de calculer quelques sha256 pour répondre au
challenge. Un petit calcul montre qu'on a 1 chance sur 500 de gagner:
```python
>>> proba = 1.0
>>> for x in zip(*seqs):
...    proba *= 1 - min(x) / 256.0
>>> proba
0.001971222333104382
```

Script solution: [solver.py](solver.py)
