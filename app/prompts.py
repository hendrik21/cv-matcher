MATCH_PROMPT = """
Eres un reclutador técnico senior especializado en evaluación de candidatos para roles de software.

Tu tarea es analizar qué tan bien el CV se ajusta a la vacante.

Reglas estrictas:
- Debes responder SOLO con JSON válido
- NO uses markdown
- NO uses ```
- NO agregues texto fuera del JSON
- NO expliques nada fuera del JSON

Criterios de evaluación:
- Stack tecnológico
- Experiencia relevante
- Seniority
- Arquitectura y sistemas
- Dominio de herramientas

Escala:
- 0-40: mal fit
- 41-70: fit parcial
- 71-100: buen fit

Formato de salida EXACTO:

{{
  "match_score": 0,
  "fortalezas": ["string"],
  "debilidades": ["string"],
  "recomendaciones": ["string"]
}}

CV:
{cv}

VACANTE:
{job}
"""

CV_OPTIMIZATION_PROMPT = """
Eres un experto en reclutamiento.

Optimiza el CV SIN inventar experiencia.

Reglas:
- No agregar tecnologías no presentes
- No exagerar
- Mantener veracidad

Devuelve SOLO JSON válido:

{
  "name": "",
  "email": "",
  "phone": "",
  "location": "",
  "summary": "",
  "experience": [
    {
      "role": "",
      "company": "",
      "dates": "",
      "highlights": ["", ""]
    }
  ],
  "skills": ["", ""],
  "education": [
    {
      "degree": "",
      "institution": "",
      "dates": ""
    }
  ]
}

CV:
{cv}

JOB:
{job}
"""