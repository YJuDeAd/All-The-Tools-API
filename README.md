# 🛠️ All The Tools - API

A REST API built from scratch to serve as a utility hub. This project is designed to automate everyday file processing tasks, data conversions, and media handling, integrating seamlessly with tools like **n8n** and local **llama models**.

> **Development Rule:** > **Zero Generative AI Code.** All logic, architecture, and code in this repository is written by hand to learn FastAPI, backend architecture, and containerization. AI is strictly limited to minimal research.

## Tech Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Server:** Uvicorn
* **Deployment:** Docker & Docker Compose
* *(More dependencies will be added later)*

## Features

### PDF Operations
- [x] PDF -> Images (Every page, Specific Range, Specific Pages)
- [x] Compress PDF
- [x] Delete specific PDF pages
- [x] PDF -> Markdown (MD)
- [x] PDF -> Plain Text
- [x] Text -> PDF
- [ ] Images -> PDF

### Data & Config Conversion
- [ ] JSON <-> YAML
- [ ] JSON <-> TOML
- [ ] JSON <-> XML

### Docker Utilities
- [ ] Docker `run` command <-> `docker-compose.yml`

### Media Processing (Coming Soon)
- [ ] Image format converter (Formats TBD)
- [ ] Video format converter (Formats TBD)
- [ ] Audio format converter (Formats TBD)
- [ ] Video -> Audio extraction
- [ ] YouTube -> Audio
- [ ] YouTube -> Video

## Current Endpoints

Below is the current list of available endpoints.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `api/v1/pdf2image` | Converts every page of a PDF to images. |
| `POST` | `api/v1/pdf2image_range` | Converts a specific start-to-end range of a PDF to images. |
| `POST` | `api/v1/pdf2image_specific`| Converts comma-separated specific pages to images. |
| `POST` | `api/v1/compress_pdf` | Reduces the file size of an uploaded PDF. |
| `POST` | `api/v1/pdf_delete_pages` | Removes specified pages from a PDF. |
| `POST` | `api/v1/pdf2md` | Extracts text and structure from a PDF to Markdown. |
| `POST` | `api/v1/pdf2txt` | Extracts raw plain text from a PDF. |
| `POST` | `api/v1/txt2pdf` | Converts a plain text file into a formatted PDF. |

## 🚀 Getting Started

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/YJuDeAd/All-The-Tools-API
cd all-the-tools-api
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

3. **Install dependencies:**
```bash
pip install -r requirements.txt

```

4. **Run the FastAPI server:**
```bash
python3 server.py

```

5. **View Documentation:** Open your browser and navigate to `http://127.0.0.1:5000/docs` to see the auto-generated Swagger UI.

## 🤝 Contributing

Since this is a personal learning project with strict rules on handwritten code, direct code contributions are currently closed. However, feature suggestions, architectural feedback, and bug reports via Issues are highly appreciated!