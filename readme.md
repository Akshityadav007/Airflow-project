```text
                           ┌────────────────────────┐
                           │        Sources         │
                           └──────────┬─────────────┘
                                      │
     ┌────────────────────────────────┼────────────────────────────────┐
     │                                │                                │
┌──────────────┐              ┌──────────────┐                   ┌────────────────┐
│  REST APIs   │              │    SQL DB    │                   │     Kafka      │
│ (Orders,     │              │  (Postgres)  │                   │ (Event Stream) │
│  Products)   │              │              │                   │                │
└──────┬───────┘              └──────┬───────┘                   └───────┬────────┘
       │                             │                                   │
       │ Batch Extraction            │ Batch Extraction                  │ Streaming
       │    (Airflow)                │    (Airflow)                      │ (Databricks)
       │                             │                                   │
  ┌────▼───────┐                 ┌───▼─────────┐                   ┌─────▼────────┐
  │  Airflow   │                 │  Airflow    │                   │ Databricks   │
  │   DAG:     │                 │   DAG:      │                   │ Streaming Job│
  │ extract_   │                 │ extract_    │                   └─────┬────────┘
  │ api_data   │                 │ sql_data    │                         │
  └────┬───────┘                 └────┬────────┘                         │
       │                              │                                  │
       │ Writes Raw Files             │ Writes Raw Files                 │ Writes Raw Events
       │                              │                                  │   (Autoloader)
       │                              │                                  │
┌──────▼────────────────────┐         │                          ┌───────▼──────────────────┐
│ AZURE BLOB - LANDING      │         │                          │    AZURE DLT CHECKPOINT  │
│  /landing/api/...         │         │                          │ (Kafka Offsets + Schema) │
│  /landing/sql/...         │         │                          └──────────┬───────────────┘
└──────────┬────────────────┘         │                                     │
           │                          │                             Streaming Auto-Load
           │                          │                                     │
┌──────────▼──────────────────────────▼─────────────────────────────────────▼───────────────────┐
│                                      BRONZE LAYER (DELTA)                                     │
│     Raw API JSON        |       Raw SQL Extracts       |          Raw Kafka Events            │
│  bronze_api_orders      |   bronze_sql_orders_items    |       bronze_stream_orders           │
└──────────┬────────────────────────────────────────────────────────────────────────────────────┘
           │
           │ Batch + Stream unified → normalized in Silver layer
           │
┌──────────▼────────────────────────────────────────────────────────────────────────────────────┐
│                                      SILVER LAYER                                             │
│   Cleaned, deduped, normalized tables for all domain entities                                 │
│      (orders, products, customers, items, inventory, etc.)                                    │
└──────────┬────────────────────────────────────────────────────────────────────────────────────┘
           │
           │ Business modeling + SCD logic (Dimensions + Facts)
           │
┌──────────▼─────────────────────────────────────────────────────────────────────────────────────┐
│                                      GOLD LAYER                                                │
│ Fact tables: Fact_Orders, Fact_Sales                                                           │
│ Dimensions: Dim_Customer, Dim_Product, Dim_Date, Dim_Store                                     │
│ BI-ready aggregated tables for reporting & ML features                                         │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```
