# UML Diagrams — WAVE Project

## 1. Class Diagram

```mermaid
classDiagram
    class Category {
        +int id_category
        +str name
        +__str__() str
    }

    class Image {
        +int id_image
        +str filename
        +int year
        +int month
        +str words
        +str rgb
        +str hsl
        +str hexadecimal
        +int red
        +int green
        +int blue
        +int hue
        +int sat
        +int bri
        +cover_url() str
        +__str__() str
    }

    class Article {
        +int id_articles
        +str title
        +str url
        +str author
        +datetime created_at
        +__str__() str
    }

    Article --> Image : image (ForeignKey)
    Article --> Category : category (ForeignKey)
```

---

## 2. Use Case Diagram

```mermaid
graph TD
    User((User))
    Researcher((Researcher))
    Admin((Admin))

    User --> UC1[Browse Covers]
    User --> UC2[Search Articles]
    User --> UC3[View Visualizations]
    User --> UC4[Send Contact Message]
    User --> UC5[View Timeline]

    Researcher --> UC1
    Researcher --> UC2
    Researcher --> UC3
    Researcher --> UC6[Access REST API]
    Researcher --> UC7[Filter by Category/Year]

    Admin --> UC8[Manage Data via Admin Panel]
    Admin --> UC9[Import Data via loaddata]
    Admin --> UC10[Deploy Application]
```

---

## 3. Sequence Diagram — Browse Covers

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Django
    participant API
    participant PostgreSQL
    participant Cloudinary

    User->>Browser: Visit /covers/
    Browser->>Django: GET /covers/
    Django->>Browser: Return covers.html

    Browser->>API: GET /api/covers/
    API->>PostgreSQL: Query Image table
    PostgreSQL-->>API: Return 362 images
    API->>Cloudinary: Build image URLs
    API-->>Browser: Return JSON with URLs

    User->>Browser: Click a cover
    Browser->>Cloudinary: GET image URL
    Cloudinary-->>Browser: Return cover image

    Browser->>API: GET /api/cover-words/?year=&month=
    API->>PostgreSQL: Query articles for that cover
    PostgreSQL-->>API: Return articles
    API-->>Browser: Return word frequency JSON
    Browser->>User: Display cover + bubble chart
```

---

## 4. Sequence Diagram — Search Articles

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Django
    participant PostgreSQL

    User->>Browser: Enter search query
    Browser->>Django: GET /api/articles/?q=keyword
    Django->>PostgreSQL: Filter articles WHERE title ILIKE %keyword%
    PostgreSQL-->>Django: Return matching articles
    Django-->>Browser: Return JSON response
    Browser->>User: Display filtered articles
```

---

## 5. Deployment Architecture Diagram

```mermaid
graph TB
    subgraph Developer
        LocalCode[Local Django App]
        GitHub[GitHub Repository]
    end

    subgraph Railway
        DjangoService[Django Service\nGunicorn]
        PostgreSQL[PostgreSQL 15\nDatabase]
    end

    subgraph External Services
        Cloudinary[Cloudinary\nMedia Storage]
        Gmail[Gmail SMTP\nEmail Service]
    end

    LocalCode -->|git push| GitHub
    GitHub -->|Auto Deploy| DjangoService
    DjangoService <-->|Internal Network| PostgreSQL
    DjangoService <-->|HTTPS| Cloudinary
    DjangoService <-->|SMTP 465| Gmail

    User((User)) -->|HTTPS| DjangoService
```

---

## 6. MCD (Modèle Conceptuel de Données)

```
┌─────────────────┐         ┌─────────────────┐
│    CATEGORY     │         │      IMAGE      │
├─────────────────┤         ├─────────────────┤
│ id_category (PK)│         │ id_image (PK)   │
│ name            │         │ filename        │
└────────┬────────┘         │ year            │
         │                  │ month           │
         │ 0,N              │ hexadecimal     │
         │                  │ hue             │
    ┌────┴────────┐         │ sat             │
    │   ARTICLE   │         │ bri             │
    ├─────────────┤    1,1  │ red/green/blue  │
    │ id_articles │◄────────┤ words           │
    │ title       │         └─────────────────┘
    │ url         │
    │ author      │
    │ created_at  │
    └─────────────┘
```
