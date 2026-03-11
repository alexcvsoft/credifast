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

## 2. Diagrama ER (Modelo de Datos)
