# 📐 Documentation UML — Wave

> Diagrammes d'architecture et modélisation du projet Wave (Django/Python)

---

## Table des matières

- [📐 Documentation UML — Wave](#-documentation-uml--wave)
  - [Table des matières](#table-des-matières)
  - [1. Diagramme de cas d'utilisation](#1-diagramme-de-cas-dutilisation)
  - [2. Diagramme de classes](#2-diagramme-de-classes)
  - [3. Diagramme de séquence — Chargement des visualisations](#3-diagramme-de-séquence--chargement-des-visualisations)
  - [4. Diagramme de séquence — Création de contenu](#4-diagramme-de-séquence--création-de-contenu)
  - [5. Diagramme d'activité](#5-diagramme-dactivité)
  - [6. Diagramme de composants](#6-diagramme-de-composants)
  - [7. Modèle Entité-Relation (ER)](#7-modèle-entité-relation-er)

---

## 1. Diagramme de cas d'utilisation

```mermaid
graph TD
    Visiteur((Visiteur))

    subgraph Application Wave
        UC1[Consulter les visualisations]
        UC2[Rechercher des articles]
        UC3[Filtrer par catégorie]
        UC4[Filtrer par date]
        UC5[Consulter un article]
        UC6[Envoyer un message de contact]
    end

    Visiteur --> UC1
    Visiteur --> UC2
    Visiteur --> UC3
    Visiteur --> UC4
    Visiteur --> UC5
    Visiteur --> UC6

    style Visiteur fill:#1A6B8A,color:#fff
    style UC1 fill:#2ABFBF,color:#fff
    style UC2 fill:#2ABFBF,color:#fff
    style UC3 fill:#2ABFBF,color:#fff
    style UC4 fill:#2ABFBF,color:#fff
    style UC5 fill:#2ABFBF,color:#fff
    style UC6 fill:#2ABFBF,color:#fff
```

---

## 2. Diagramme de classes

```mermaid
classDiagram
    class Image {
        +int id_image
        +String filename
        +int year
        +int month
        +String words
        +String rgb
        +String hsl
        +String hexadecimal
        +int red
        +int green
        +int blue
        +int hue
        +int sat
        +int bri
    }

    class Article {
        +int id_articles
        +String title
        +String url
        +String author
        +DateTime created_at
    }

    class Category {
        +int id_category
        +String name
    }

    Image "1" --> "0..*" Article : possède
    Category "0..1" --> "0..*" Article : classe

    style Image fill:#1A6B8A,color:#fff
    style Article fill:#2ABFBF,color:#fff
    style Category fill:#E8F4F8,color:#1A6B8A
```

---

## 3. Diagramme de séquence — Chargement des visualisations

```mermaid
sequenceDiagram
    actor V as Visiteur
    participant B as Navigateur
    participant D as Django View
    participant DB as PostgreSQL

    V->>B: Ouvre l'application
    B->>D: GET /
    D->>DB: SELECT images, articles, categories
    DB-->>D: Données
    D-->>B: Page HTML + visualisations
    B-->>V: Affichage des graphiques

    V->>B: Interaction (filtre / clic)
    B->>D: GET /articles/?filter=...
    D->>DB: SELECT articles WHERE condition
    DB-->>D: Résultats
    D-->>B: Mise à jour affichage
    B-->>V: Résultats filtrés
```

---

## 4. Diagramme de séquence — Création de contenu

```mermaid
sequenceDiagram
    actor U as Utilisateur
    participant V as Django View
    participant F as Formulaire
    participant DB as PostgreSQL

    U->>V: POST /articles/create
    V->>F: Validation des données

    alt Formulaire valide
        F-->>V: cleaned_data
        V->>DB: INSERT Article
        DB-->>V: Article créé
        V-->>U: Redirection article
    else Formulaire invalide
        F-->>V: erreurs
        V-->>U: Affichage erreurs
    end
```

---

## 5. Diagramme d'activité

```mermaid
flowchart TD
    Start([Début]) --> Home[Page d'accueil]
    Home --> Action{Action utilisateur}

    Action --> Viz[Voir visualisations]
    Action --> Search[Rechercher articles]
    Action --> Filter[Filtrer données]
    Action --> Open[Consulter article]

    Viz --> ViewImages[Analyse des images]
    Search --> DB[(Base de données)]
    Filter --> DB
    DB --> Results[Résultats]
    Open --> ArticleView[Affichage article]

    ViewImages --> Home
    Results --> Home
    ArticleView --> Home



    style Start fill:#1A6B8A,color:#fff
    style Home fill:#2ABFBF,color:#fff
    style Action fill:#E8F4F8,color:#1A6B8A
    style Viz fill:#2ABFBF,color:#fff
    style Search fill:#2ABFBF,color:#fff
    style Filter fill:#2ABFBF,color:#fff
    style Open fill:#2ABFBF,color:#fff
    style DB fill:#1A6B8A,color:#fff
    style Results fill:#E8F4F8,color:#1A6B8A
    style ViewImages fill:#E8F4F8,color:#1A6B8A
    style ArticleView fill:#E8F4F8,color:#1A6B8A
```

---

## 6. Diagramme de composants

```mermaid
graph TB
    Browser[Navigateur]

    subgraph Django
        URLs[urls.py]
        Views[Views]
        Models[Models - Image, Article, Category]
        Templates[HTML Templates]
    end

    DB[(PostgreSQL)]
    JSON[Fichiers JSON]

    JSON --> Models
    Browser --> URLs
    URLs --> Views
    Views --> Models
    Models --> DB
    Views --> Templates
    Templates --> Browser


    style Browser fill:#1A6B8A,color:#fff
    style URLs fill:#2ABFBF,color:#fff
    style Views fill:#2ABFBF,color:#fff
    style Models fill:#2ABFBF,color:#fff
    style Templates fill:#2ABFBF,color:#fff
    style DB fill:#1A6B8A,color:#fff
    style JSON fill:#E8F4F8,color:#1A6B8A
```

---

## 7. Modèle Entité-Relation (ER)

```mermaid
erDiagram
    IMAGE {
        int id_image PK
        string filename
        int year
        int month
        string words
        string rgb
        string hsl
        string hexadecimal
        int red
        int green
        int blue
        int hue
        int sat
        int bri
    }

    ARTICLE {
        int id_articles PK
        string title
        string url
        string author
        datetime created_at
        int id_image FK
        int id_category FK
    }

    CATEGORY {
        int id_category PK
        string name
    }

    IMAGE ||--o{ ARTICLE : "contient"
    CATEGORY ||--o{ ARTICLE : "classe"
```

---


