# CV Matcher (AI Job Tracker)

CV Matcher es una herramienta CLI que automatiza el seguimiento de aplicaciones laborales utilizando IA. Permite analizar vacantes, evaluar compatibilidad con tu CV, generar CV optimizados y llevar un tracking de estados de aplicación.

---

## 🚀 Funcionalidades

- 📄 Carga automática de CV (TXT o PDF)
- 🧠 Evaluación de compatibilidad CV vs vacante usando LLM (Ollama)
- 📊 Score de match (0–100)
- ✍️ Generación de CV optimizado (ATS-friendly)
- 📑 Exportación a PDF
- 🔎 Scraping de descripciones de empleo (Playwright)
- 📌 Tracking de aplicaciones laborales con estados
- 🧾 CLI global tipo comando (`cv-matcher`)

---

## 🧱 Arquitectura del proyecto

El proyecto está organizado en módulos independientes dentro del paquete `app/`:

```
app/
 ├── cli.py              # Interfaz CLI principal
 ├── tracker.py         # Lógica de tracking de jobs
 ├── matcher.py        # Evaluación CV vs Job (LLM)
 ├── prompts.py        # Prompts para LLM
 ├── cv_generator.py   # Optimización de CV
 ├── pdf_generator.py  # Exportación a PDF
 ├── pdf_parser.py     # Lectura de CV en PDF
 ├── parser.py         # Lectura de CV en TXT
 ├── scraper.py        # Scraping de ofertas
 ├── embeddings.py     # (futuro / IA semántica)
 └── main.py           # punto de entrada opcional
```

---

## ⚙️ Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/hendrik21/cv-matcher.git
cd cv-matcher
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Instalar como comando global (modo desarrollo)
```bash
pip install -e .
```

---

## 🧠 Requisitos

- Python 3.10+
- Ollama instalado localmente
- Modelo recomendado:
```bash
ollama run qwen2.5:7b
```

---

## 🧪 Uso del CLI

### ➕ Agregar una vacante
```bash
cv-matcher add --title "Backend Developer" --company "Emapta"
```
Opcional con scraping:
```bash
cv-matcher add --title "Backend Developer" --company "Emapta" --url <job-url>
```

---

### 📋 Listar vacantes
```bash
cv-matcher list
```

---

### 🔄 Actualizar estado
```bash
cv-matcher update --id <job-id> --status "Applied"
```

Estados disponibles:
- Not applied
- Applied
- First interview
- Technical interview
- Last interview
- Offer received
- Rejected

---

## 🧠 Lógica de IA

El sistema utiliza un LLM local (Ollama) para:

- Evaluar compatibilidad CV vs job description
- Generar score de match
- Detectar fortalezas y debilidades
- Recomendar mejoras de CV

Threshold actual:
```
75 → genera CV optimizado automáticamente
```

---

## 📌 Tracking de aplicaciones

Cada job guarda:

- ID único
- Empresa
- Título
- Estado
- Score de match
- Evaluación del LLM
- CV optimizado (si aplica)
- PDF generado (si aplica)

---

## 🧹 Buenas prácticas

Archivos ignorados en git:

```
data/cvs/
data/output/
data/tracking.json
__pycache__/
*.pyc
.venv/
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas.

1. Haz fork del proyecto
2. Crea una rama feature
3. Haz commit de tus cambios
4. Abre un Pull Request

---

## 📄 Licencia

MIT License

Copyright (c) 2026 Hendrik López

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

---

## 🔮 Roadmap

- [ ] Embeddings semánticos para matching más preciso
- [ ] Dashboard web
- [ ] Multi-CV profiles
- [ ] Integración con LinkedIn scraping
- [ ] Auto-apply inteligente (modo autopilot)

---

## ⚡ Estado del proyecto

En desarrollo activo — versión experimental de AI Job Tracker CLI.

