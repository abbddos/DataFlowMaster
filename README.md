# 🚀 DataFlowMaster: Real-Time Refugee Analytics Pipeline

> **From Crisis to Clarity: Streamlining Humanitarian Data for Faster Emergency Response**

## 🌟 What is This?

A **real-time data pipeline** that simulates refugee registration during humanitarian crises, processes the data in real-time, and provides live analytics to aid organizations like UNHCR/ICRC.

### 🎯 The Problem
Humanitarian crises generate massive data chaos:
- 📧 **Excel spreadsheets** emailed between agencies  
- 📊 **Disconnected data silos** across camps
- ⏰ **Days of delay** in critical decision-making
- 📉 **No real-time visibility** into evolving needs

### 💡 Our Solution
A **modern data pipeline** that turns chaos into actionable insights in **real-time**:


## 🏗️ Architecture

```mermaid
graph LR
    A[📱 Data Generator] --> B[🌐 Flask API]
    B --> C[⚡ Kafka]
    C --> D[🔬 Polars Analytics]
    D --> E[📡 WebSocket]
    E --> F[📊 Next.js Dashboard]


## 🧩 Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Data Generator** | Python + Requests | Simulates refugee registrations from multiple camps |
| **REST API** | Flask + SQLite | Receives and stores refugee data |
| **Message Broker** | Apache Kafka | Real-time data streaming |
| **Analytics Engine** | Polars (Python) | Real-time demographic analytics |
| **Real-time Bridge** | WebSocket | Live data broadcasting |
| **Dashboard** | Next.js | Visualization for decision makers |

## 🚀 Quick Start

### Prerequisites
```bash
python 3.8+, Kafka, Node.js 16+



