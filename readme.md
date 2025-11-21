                           ┌────────────────────────┐
                           │        Sources         │
                           └──────────┬─────────────┘
                                      │
     ┌────────────────────────────────┼────────────────────────────────┐
     │                                │                                │
┌──────────────┐              ┌──────────────┐                   ┌────────────────┐
│  REST APIs   │              │  SQL DB      │                   │     Kafka      │
│ (Orders,     │              │ (Postgres)   │                   │ (Event Streams)│
│  Products)   │              │              │                   │                │
└──────┬───────┘              └──────┬───────┘                   └───────┬────────┘
       │                             │                                   │
       │ Batch Extraction            │ Batch Extraction                  │ Streaming
       │ (Airflow)                   │ (Airflow)                         │ (Databricks)
       │                             │                                   │
  ┌────▼───────┐                 ┌───▼─────────┐                   ┌─────▼────────┐
  │ Airflow    │                 │ Airflow     │                   │ Databricks   │
  │ DAG:       │                 │ DAG:        │                   │ Streaming Job│
  │ extract_   │                 │ extract_    │                   └─────┬────────┘
  │ api_data   │                 │ sql_data    │                         │
  └────┬───────┘                 └────┬────────┘                         │
       │                              │                                  │
       │ Writes Raw Files             │ Writes Raw Files                 │ Writes Raw Events
       │                              │                                  │ (Autoloader)
       │                              │                                  │
┌──────▼────────────────────┐         │                          ┌───────▼──────────────────┐
│ AZURE BLOB - LANDING      │         │                          │    AZURE DLT CHECKPOINT  │
│ /landing/api/...          │         │                          │  (Kafka Offsets + Schema)│
│ /landing/sql/...          │         │                          └──────────┬───────────────┘
└──────────┬────────────────┘         │                                     │
           │                          │                                     │
           │                          │                             Streaming Auto-Load
           │                          │                                     │
┌──────────▼──────────────────────────▼─────────────────────────────────────▼───────────────────┐
│                               BRONZE LAYER (DELTA)                                            │
│       Raw API JSON      |      Raw SQL Extracts       |          Raw Kafka Events             │
│   bronze_api_orders     |   bronze_sql_orders_items   |       bronze_stream_orders            │
└──────────┬────────────────────────────────────────────────────────────────────────────────────┘
           │
           │ Batch & Stream both unified → normalized in Silver layer
           │
┌──────────▼────────────────────────────────────────────────────────────────────────────────────┐
│                                      SILVER LAYER                                             │
│  Cleaned, deduped, normalized tables for all domain entities (orders, products, customers)    │
└──────────┬────────────────────────────────────────────────────────────────────────────────────┘
           │
           │ Business modeling & SCD logic
           │
┌──────────▼─────────────────────────────────────────────────────────────────────────────────────┐
│                                      GOLD LAYER                                                │
│  Fact Tables (Fact_Orders, Fact_Sales) + Dimensions (Dim_Customer, Dim_Product, Dim_Date)      │
│  BI-ready aggregated tables                                                                    │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
