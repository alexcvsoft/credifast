# CrediFast - Documentación de Arquitectura

Este documento describe la arquitectura, el modelo de datos y el flujo de procesamiento de la aplicación CrediFast.

---

## 1. Diagrama de Arquitectura

```mermaid
flowchart TB
    Client["Client"] --> API["Django REST API<br>CrediFast<br><br>Endpoints:<br>POST /applications<br>POST /applications/{id}/documents<br>GET /applications/{id}<br>GET /scorecredito"]
    API --> AppService["Application Service<br>Create application<br>Store user data"] & DocService["Document Service<br>Upload documents<br>Process files"]
    AppService --> DecisionEngine["Decision Engine<br>Evaluate application<br>Approve / Reject"] & Database[("PostgreSQL Database<br>Applications<br>Documents<br>Decisions<br>Rule Logs")]
    DecisionEngine --> ScoreService["Credit Score Service<br>GET /scorecredito<br>Returns 300-900"] & RulesEngine["Rules Engine<br>score &gt;= 500<br>monthly_income &gt;= 10000<br>bank_history &gt;= 6<br>age between 25 and 60<br>is_married = true OR has_children = true<br>declared_address = document_address"] & Database
    DocService --> DocumentAI["Document AI<br>Extract name, address, date<br>Validate address consistency"] & Database

    style Client fill:#f39c12,color:white
    style API fill:#3498db,color:white
    style AppService fill:#2ecc71,color:white
    style DocService fill:#2ecc71,color:white
    style DecisionEngine fill:#2ecc71,color:white
    style Database fill:#7f8c8d,color:white
    style ScoreService fill:#f1c40f,color:black
    style RulesEngine fill:#f1c40f,color:black
    style DocumentAI fill:#f1c40f,color:black
```    
**Decisiones de diseño:**

- Separamos la lógica de aplicación (AppService) y la de documentos (DocService) para aislar responsabilidades.

- El Decision Engine centraliza la evaluación de reglas y decisiones de crédito.

- Los servicios de apoyo (ScoreService, RulesEngine, DocumentAI) mantienen la lógica especializada fuera del core de la API.

- La BD relacional (PostgreSQL) almacena aplicaciones, documentos, decisiones y logs de reglas para trazabilidad.

## 2. Diagrama ER (Modelo de Datos)
```mermaid
erDiagram
APPLICATION {
    uuid id PK
    string full_name
    int age
    boolean is_married
    boolean has_children
    decimal monthly_income
    string declared_address
    int bank_history_months
    int credit_score
    datetime created_at
}

ADDRESS_PROOF {
    uuid id PK
    uuid application_id FK
    string file_url
    string extracted_name
    string extracted_address
    date extracted_date
}

DECISION {
    uuid id PK
    uuid application_id FK
    boolean approved
    string reason
    datetime evaluated_at
}

RULE_LOG {
    uuid id PK
    uuid decision_id FK
    string rule_name
    boolean passed
    string message
}

APPLICATION ||--|| ADDRESS_PROOF : includes
APPLICATION ||--|| DECISION : generates
DECISION ||--o{ RULE_LOG : produces
```
**Decisiones de diseño:**

- Cada APPLICATION puede tener un comprobante de domicilio y una decisión asociada.

- RULE_LOG permite auditar qué reglas se evaluaron y cuáles pasaron/fallaron.

- La normalización evita datos duplicados y asegura consistencia entre aplicaciones, documentos y decisiones.

## 3. Diagrama de Flujo (Proceso de Aplicación)
```mermaid
flowchart TD
Start([Start])

CreateApp[Create Application]
SaveApp[(Insert APPLICATION)]

GetScore[Call Credit Score Service]
UpdateScore[(Update APPLICATION.credit_score)]

UploadDoc[Upload Address Proof]
SaveDoc[(Insert ADDRESS_PROOF)]

ProcessDoc[Document AI Extraction]
UpdateDoc[(Update extracted fields)]

EvaluateRules[Evaluate Rules Engine]

Decision{All rules pass?}

Approve[Create DECISION: approved]
Reject[Create DECISION: rejected]

LogRules[(Insert RULE_LOG records)]

End([End])

Start --> CreateApp
CreateApp --> SaveApp
SaveApp --> GetScore
GetScore --> UpdateScore
UpdateScore --> UploadDoc
UploadDoc --> SaveDoc
SaveDoc --> ProcessDoc
ProcessDoc --> UpdateDoc
UpdateDoc --> EvaluateRules
EvaluateRules --> Decision

Decision -->|Yes| Approve
Decision -->|No| Reject

Approve --> LogRules
Reject --> LogRules

LogRules --> End
```

**Decisiones de diseño:**

- Se prioriza el flujo síncrono de creación de aplicación y subida de documentos.

- La integración con servicios externos (Credit Score y Document AI) ocurre después de almacenar los datos iniciales para asegurar persistencia.

- Se mantiene un registro completo de reglas evaluadas para trazabilidad y auditoría.

- La decisión final solo se genera cuando todas las reglas se evaluaron correctamente, asegurando consistencia y control de riesgos.

