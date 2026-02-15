# Novel Library & Converter

A modular, high-performance web-based reader and converter for light novels. This project has undergone a complete **ground-up rewrite**, evolving from a static script collection into a modern, containerized asynchronous web application.

## 📖 Project Evolution

The project originated as a set of basic data processing scripts (`JSON` > `Markdown` > `Static HTML`) served via a simple `python -m http.server`.

To achieve professional-grade scalability and performance, the architecture was entirely re-engineered:

* **Data Layer**: Migrated from static files to **SQLite** with full data normalization. Implemented a relational schema using `JOIN` queries to optimize the link between books and chapters.
* **Backend**: Rebuilt on **Python 3.10.6** using **FastAPI**, providing a robust asynchronous API for content delivery.
* **Frontend**: Decoupled the monolithic `index.html` into a modular architecture using **ES6 Modules**. Introduced a dynamic **Dark Mode** engine with system-preference detection and manual override.
* **DevOps**: Implemented full containerization and a **GitLab CI/CD** pipeline for automated testing and deployment to a production **Ubuntu 22.04** environment.

## 🛠 Tech Stack

### Backend

* **Runtime**: Python 3.10.6
* **Framework**: FastAPI (Asynchronous)
* **Database**: SQLite with `aiosqlite`

### Frontend

* **Logic**: Vanilla JavaScript (ES6 Modules)
* **Styling**: CSS3 with Custom Properties (Variables)
* **State**: LocalStorage for persistent theme settings

### Infrastructure

* **Development**: Windows 11 Pro / Git Bash
* **Production**: Ubuntu 22.04 (Xeon E5-2697)
* **Virtualization**: Docker & Private Registry
* **CI/CD**: GitLab Pipelines

## 🚀 Getting Started

### Prerequisites

* Docker & Docker Compose
* Python 3.10.6 (for local development)

### Quick Start

1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd novel_converter

```


2. **Deploy via Docker**
```bash
docker compose up -d

```


The application will be available at `http://localhost:8000`.

## 📂 Project Structure

```text
.
├── static/                 # Modular Frontend Assets
│   ├── css/
│   │   ├── base.css        # Layout & Core UI
│   │   └── dark_mode.css   # Theme Variables
│   ├── js/
│   │   ├── app.js          # Business Logic & API Interaction
│   │   └── dark_mode_support.js
│   └── index.html          # Clean HTML Skeleton
├── main.py                 # FastAPI Application Entry
├── .gitlab-ci.yml          # CI/CD Pipeline Configuration
└── Dockerfile              # Container Build Specification

```

## ⚙️ CI/CD Workflow

We adhere to a strict development lifecycle:

1. **Feature/Refactor Branch**: All changes are developed in dedicated branches.
2. **Test-Build**: GitLab CI automatically builds the image and verifies dependencies.
3. **Merge Request**: Merging to `main` is restricted until `Pipelines must succeed` check passes.
4. **Auto-Deploy**: Successful merges trigger an automatic push to the private registry and deployment to the **Xeon E5** server.

## 📝 Recent Milestones

* `refactor`: Fully decoupled frontend assets for improved maintainability.
* `feat`: Integrated adaptive dark mode with manual toggle.
* `fix`: Resolved CI/CD syntax for Docker login and insecure registry support.
* `db`: Implemented normalized database schema for efficient chapter indexing.

---

*Developed by Roy @ HPC-TigerHabitat*