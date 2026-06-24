# Documentation Technique - Coffre-fort Numérique

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du projet](#architecture-du-projet)
3. [Stéganographie LSB - Principe](#stéganographie-lsb---principe)
4. [Services - Logique métier](#services---logique-métier)
5. [Interface utilisateur - Views](#interface-utilisateur---views)
6. [Métriques de qualité](#métriques-de-qualité)
7. [Flux de données](#flux-de-données)

---

## 1. Vue d'ensemble

### Qu'est-ce que ce projet ?

Ce projet est une **application de stéganographie** qui permet de cacher des messages secrets dans des images de manière invisible à l'œil nu. La technique utilisée est appelée **LSB (Least Significant Bit)**.

### Principe de base

**Stéganographie** = Art de cacher des informations dans d'autres données
- ❌ Pas de chiffrement (version simplifiée)
- ✅ Le message est caché dans les pixels de l'image
- ✅ Les modifications sont invisibles visuellement

---

## 2. Architecture du projet

### Structure des dossiers

```
ProjetDecodeur/
│
├── app.py                      # Point d'entrée principal
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation utilisateur
│
├── services/                   # COUCHE LOGIQUE (Backend)
│   ├── __init__.py
│   ├── crypto_service.py       # [NON UTILISÉ maintenant]
│   ├── stegano_service.py      # ⭐ Stéganographie LSB
│   ├── metrics_service.py      # 📊 Calcul MSE/PSNR
│   └── file_service.py         # 📁 Gestion de fichiers
│
└── views/                      # COUCHE PRÉSENTATION (Frontend)
    ├── __init__.py
    ├── home.py                 # Page d'accueil
    ├── encode.py               # Page encodage
    ├── decode.py               # Page décodage
    └── analyze.py              # Page analyse
```

### Séparation des responsabilités

| Couche | Rôle | Fichiers |
|--------|------|----------|
| **Services** | Logique métier, algorithmes | `services/*.py` |
| **Views** | Interface utilisateur, affichage | `views/*.py` |
| **App** | Configuration, navigation | `app.py` |

---

## 3. Stéganographie LSB - Principe

### Comment fonctionne LSB ?

#### 3.1 Représentation des pixels

Une image est composée de **pixels**. Chaque pixel a des valeurs RGB (Rouge, Vert, Bleu) :

```
Pixel = (Rouge: 0-255, Vert: 0-255, Bleu: 0-255)
```

Exemple d'un pixel :
```
Pixel = (Red: 142, Green: 98, Blue: 201)
```

#### 3.2 Représentation binaire

Chaque valeur de couleur (0-255) est codée sur **8 bits** :

```
142 en décimal = 10001110 en binaire
                 ^^^^^^^^
                 |||||||└─ Bit 0 (LSB - Least Significant Bit)
                 ||||||└── Bit 1
                 |||||└─── Bit 2
                 ||||└──── Bit 3
                 |||└───── Bit 4
                 ||└────── Bit 5
                 |└─────── Bit 6
                 └──────── Bit 7 (MSB - Most Significant Bit)
```

#### 3.3 Le bit de poids faible (LSB)

Le **dernier bit** (bit 0) s'appelle le **LSB (Least Significant Bit)**.

**Propriété importante** : Modifier le LSB change très peu la valeur :

```
10001110 (142) → LSB = 0
10001111 (143) → LSB = 1  (différence de 1 seulement !)
```

Cette différence de 1 est **invisible à l'œil humain** ! 👀

#### 3.4 Cacher un message

Pour cacher un message, on :

1. **Convertit le message en binaire**
   ```
   Message: "Hi"
   H = 72  = 01001000
   i = 105 = 01101001
   ```

2. **Modifie les LSB des pixels**
   ```
   Pixel 1 (Rouge) : 10001110 → 10001110 (LSB = 0 pour stocker 0)
   Pixel 1 (Vert)  : 11010011 → 11010011 (LSB = 1 pour stocker 1)
   Pixel 1 (Bleu)  : 10100110 → 10100110 (LSB = 0 pour stocker 0)
   ...
   ```

3. **Résultat** : Le message est caché dans l'image !

### Exemple concret

#### Image originale (3 pixels RGB)
```
Pixel 1: (142, 98, 201)
Pixel 2: (75, 210, 33)
Pixel 3: (189, 54, 120)
```

#### Convertir en binaire
```
Pixel 1: (10001110, 01100010, 11001001)
Pixel 2: (01001011, 11010010, 00100001)
Pixel 3: (10111101, 00110110, 01111000)
```

#### Message à cacher : "A" = 65 = 01000001

On va utiliser 8 canaux (8 bits) :

```
Bit à cacher : 0 → Pixel 1 Rouge : 10001110 → 10001110 (déjà 0)
Bit à cacher : 1 → Pixel 1 Vert  : 01100010 → 01100011 (changé)
Bit à cacher : 0 → Pixel 1 Bleu  : 11001001 → 11001000 (changé)
Bit à cacher : 0 → Pixel 2 Rouge : 01001011 → 01001010 (changé)
Bit à cacher : 0 → Pixel 2 Vert  : 11010010 → 11010010 (déjà 0)
Bit à cacher : 0 → Pixel 2 Bleu  : 00100001 → 00100000 (changé)
Bit à cacher : 0 → Pixel 2 Rouge : 10111101 → 10111100 (changé)
Bit à cacher : 1 → Pixel 3 Vert  : 00110110 → 00110111 (changé)
```

#### Image modifiée
```
Pixel 1: (142, 99, 200)   ← Changements minimes !
Pixel 2: (74, 210, 32)
Pixel 3: (188, 55, 120)
```

**Différence visuelle** : INVISIBLE ! Les changements sont de ±1 seulement.

---

## 4. Services - Logique métier

### 4.1 SteganoService (`stegano_service.py`)

C'est le **cœur de l'application**. Il gère la stéganographie.

#### Méthode : `hide_message()`

**Rôle** : Cacher un message dans une image

```python
def hide_message(image_path: str, message: str, output_path: str) -> dict:
```

**Étapes** :
1. Ouvre l'image avec la bibliothèque `stegano`
2. Vérifie que l'image a assez de capacité pour le message
3. Utilise `lsb.hide()` pour cacher le message (modification des LSB)
4. Sauvegarde la nouvelle image
5. Retourne les statistiques

**Code interne (bibliothèque stegano)** :
- Convertit le message en bits
- Pour chaque bit du message, modifie le LSB d'un pixel
- Ajoute des métadonnées pour savoir où s'arrête le message

#### Méthode : `reveal_message()`

**Rôle** : Récupérer un message caché

```python
def reveal_message(image_path: str) -> str:
```

**Étapes** :
1. Ouvre l'image
2. Utilise `lsb.reveal()` pour lire les LSB
3. Reconstruit le message original
4. Retourne le message

#### Méthode : `calculate_capacity()`

**Rôle** : Calculer combien de données peuvent être cachées

```python
def calculate_capacity(image_path: str) -> dict:
```

**Formule** :
```
Capacité (bits) = Largeur × Hauteur × Nombre_de_canaux
Capacité (bytes) = Capacité (bits) ÷ 8
```

**Exemple** :
```
Image 1000x800 pixels RGB (3 canaux)
Capacité = 1000 × 800 × 3 = 2,400,000 bits
         = 300,000 bytes
         ≈ 300 KB de message
```

---

### 4.2 MetricsService (`metrics_service.py`)

**Rôle** : Calculer la qualité de l'image après modification

#### Méthode : `calculate_mse()`

**MSE = Mean Squared Error** (Erreur Quadratique Moyenne)

**Formule mathématique** :
```
MSE = (1/N) × Σ(I₁[i,j] - I₂[i,j])²

Où :
- N = nombre total de pixels
- I₁ = image originale
- I₂ = image modifiée
```

**Interprétation** :
- MSE = 0 → Images identiques
- MSE < 1 → Différence imperceptible
- MSE > 10 → Différence visible

**Code simplifié** :
```python
def calculate_mse(original, modified):
    # Convertir en tableau numpy
    img1 = cv2.imread(original)
    img2 = cv2.imread(modified)
    
    # Calculer la différence au carré
    mse = np.mean((img1 - img2) ** 2)
    
    return mse
```

#### Méthode : `calculate_psnr()`

**PSNR = Peak Signal-to-Noise Ratio** (Rapport Signal/Bruit)

**Formule mathématique** :
```
PSNR = 10 × log₁₀(MAX² / MSE)

Où :
- MAX = valeur maximale d'un pixel (255 pour images 8-bit)
- MSE = Mean Squared Error
```

**Interprétation** :
- PSNR > 50 dB → Pratiquement identiques
- PSNR > 40 dB → Excellente qualité (invisible)
- PSNR > 30 dB → Bonne qualité (difficile à voir)
- PSNR < 20 dB → Modifications visibles

**Pourquoi c'est important** :
Si PSNR > 30 dB, cela garantit que les modifications sont **invisibles à l'œil nu** !

---

### 4.3 FileService (`file_service.py`)

**Rôle** : Gérer les fichiers uploadés et les conversions

#### Méthodes principales :

1. **`validate_image()`** : Vérifie que le fichier est une image valide
2. **`save_uploaded_file()`** : Sauvegarde le fichier uploadé dans un dossier temporaire
3. **`ensure_png_format()`** : Convertit l'image en PNG (important pour LSB !)

**Pourquoi PNG ?**
- PNG = format **sans perte** (lossless)
- JPEG = format **avec perte** (lossy) → peut corrompre le message caché !

---

## 5. Interface utilisateur - Views

### 5.1 Page Encoder (`encode.py`)

**Workflow utilisateur** :

```
┌─────────────────────────────────────────┐
│ 1️⃣ Sélectionner une image              │
│    → Upload de l'image                  │
│    → Affichage de la capacité           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2️⃣ Entrer le message                   │
│    → Saisie du texte secret             │
│    → Vérification de la taille          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3️⃣ Encoder                             │
│    → Clic sur "Cacher le message"       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 📊 Résultats                            │
│    → Image encodée                      │
│    → Métriques MSE/PSNR                 │
│    → Bouton de téléchargement           │
└─────────────────────────────────────────┘
```

**Code clé** :
```python
# Étape 1 : Cacher le message
result = SteganoService.hide_message(image_path, message, output_path)

# Étape 2 : Calculer les métriques
metrics = MetricsService.generate_report(original_image, encoded_image)

# Étape 3 : Afficher les résultats
st.image(output_path)
st.metric("PSNR", metrics['psnr'])
```

---

### 5.2 Page Décoder (`decode.py`)

**Workflow utilisateur** :

```
┌─────────────────────────────────────────┐
│ 1️⃣ Sélectionner l'image encodée        │
│    → Upload de l'image                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2️⃣ Décoder                             │
│    → Clic sur "Extraire le message"     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 📝 Message Secret                       │
│    → Affichage du message               │
│    → Statistiques (taille, lignes)      │
└─────────────────────────────────────────┘
```

**Code clé** :
```python
# Extraire le message
message = SteganoService.reveal_message(image_path)

# Afficher
st.markdown(f"<p style='color: #000000;'>{message}</p>")
```

---

### 5.3 Page Analyser (`analyze.py`)

**Deux modes** :

#### Mode 1 : Capacité de stockage
- Calcule combien de bytes peuvent être cachés
- Affiche des équivalences (caractères, mots, pages)

#### Mode 2 : Comparaison d'images
- Compare deux images (avant/après)
- Calcule MSE et PSNR
- Affiche l'échelle de qualité

---

## 6. Métriques de qualité

### Pourquoi calculer MSE et PSNR ?

**Objectif** : Vérifier que les modifications sont **invisibles** !

### Tableau d'interprétation

| PSNR (dB) | MSE | Qualité | Visibilité |
|-----------|-----|---------|------------|
| > 50 | < 0.01 | Parfait | Identique |
| 40-50 | 0.01-1 | Excellent | Invisible |
| 30-40 | 1-10 | Bon | Très difficile à voir |
| 20-30 | 10-100 | Acceptable | Légèrement visible |
| < 20 | > 100 | Faible | Visible |

### Exemple réel

```
Image originale vs Image avec message caché :
- MSE = 0.52
- PSNR = 41.23 dB
→ Qualité : Excellent
→ Visibilité : Invisible à l'œil nu ✅
```

---

## 7. Flux de données

### Encodage complet

```
┌─────────────┐
│   Utilisateur   │
└───────┬─────┘
        │ 1. Upload image.png
        ↓
┌─────────────────┐
│  FileService    │ ← Validation & Sauvegarde
└───────┬─────────┘
        │ 2. image_path
        ↓
┌─────────────────┐
│ SteganoService  │ ← Vérification capacité
└───────┬─────────┘
        │ 3. Capacité OK
        ↓
┌─────────────────┐
│   Utilisateur   │ ← Entre le message "Secret"
└───────┬─────────┘
        │ 4. Message "Secret"
        ↓
┌─────────────────┐
│ SteganoService  │ ← lsb.hide(image, "Secret")
│                 │   Modifie les LSB des pixels
└───────┬─────────┘
        │ 5. Image encodée
        ↓
┌─────────────────┐
│ MetricsService  │ ← Calcule MSE & PSNR
└───────┬─────────┘
        │ 6. MSE=0.5, PSNR=42 dB
        ↓
┌─────────────────┐
│   Streamlit     │ ← Affiche résultats
└─────────────────┘
```

### Décodage complet

```
┌─────────────┐
│  Utilisateur    │
└───────┬─────┘
        │ 1. Upload image_encoded.png
        ↓
┌─────────────────┐
│  FileService    │ ← Sauvegarde
└───────┬─────────┘
        │ 2. image_path
        ↓
┌─────────────────┐
│ SteganoService  │ ← lsb.reveal(image)
│                 │   Lit les LSB des pixels
│                 │   Reconstruit le message
└───────┬─────────┘
        │ 3. Message "Secret"
        ↓
┌─────────────────┐
│   Streamlit     │ ← Affiche le message
└─────────────────┘
```

---

## 8. Résumé des concepts clés

### Stéganographie LSB
- ✅ Cache des données dans les bits de poids faible
- ✅ Modifications invisibles (±1 par pixel)
- ✅ Pas de chiffrement (message en clair dans l'image)

### Capacité
- 📐 Dépend de la taille de l'image
- 📐 Formule : largeur × hauteur × canaux ÷ 8 bytes

### Métriques
- 📊 MSE : mesure la différence moyenne
- 📊 PSNR : mesure la qualité (> 30 dB = invisible)

### Architecture
- 🏗️ Services : logique métier (algorithmes)
- 🎨 Views : interface utilisateur (Streamlit)
- 🔧 App : configuration et navigation

---

## 9. Points importants

### ⚠️ Limitations

1. **Format d'image** : Utiliser PNG (pas JPEG !)
2. **Taille du message** : Limitée par la taille de l'image
3. **Sécurité** : Le message n'est PAS chiffré (visible si quelqu'un cherche)
4. **Compression** : Ne pas compresser l'image après encodage !

### ✅ Avantages

1. **Invisible** : PSNR > 30 dB garantit l'invisibilité
2. **Simple** : Pas de mot de passe à retenir
3. **Rapide** : Encodage/décodage instantané
4. **Scientifique** : Base mathématique solide (LSB)

---

## 10. Pour aller plus loin

### Améliorations possibles

1. **Chiffrement** : Réactiver le système AES pour la sécurité
2. **Fichiers** : Cacher des fichiers complets (pas seulement du texte)
3. **Compression** : Compresser le message avant insertion
4. **Multi-images** : Répartir un gros message sur plusieurs images
5. **Détection** : Ajouter une analyse stégano pour détecter les images suspectes

---

**Fin de la documentation technique** 📚
