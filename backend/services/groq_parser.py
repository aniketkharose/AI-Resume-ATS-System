import json
from typing import Any

from groq import Groq

from backend.core.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
)


class GroqParserError(Exception):
    """Base exception for Groq resume parsing errors."""


# ============================================================
# STRUCTURED RESUME SCHEMA
# ============================================================

RESUME_SCHEMA = {
    "type": "object",
    "properties": {
        "contact": {
            "type": "object",
            "properties": {
                "name": {
                    "type": ["string", "null"]
                },
                "email": {
                    "type": ["string", "null"]
                },
                "phone": {
                    "type": ["string", "null"]
                },
                "location": {
                    "type": ["string", "null"]
                },
                "linkedin": {
                    "type": ["string", "null"]
                },
                "github": {
                    "type": ["string", "null"]
                },
            },
            "required": [
                "name",
                "email",
                "phone",
                "location",
                "linkedin",
                "github",
            ],
            "additionalProperties": False,
        },

        "summary": {
            "type": ["string", "null"]
        },

        "skills": {
            "type": "array",
            "items": {
                "type": "string"
            },
        },

        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "degree": {
                        "type": "string"
                    },
                    "institution": {
                        "type": "string"
                    },
                    "location": {
                        "type": ["string", "null"]
                    },
                    "start_date": {
                        "type": ["string", "null"]
                    },
                    "end_date": {
                        "type": ["string", "null"]
                    },
                    "details": {
                        "type": ["string", "null"]
                    },
                },
                "required": [
                    "degree",
                    "institution",
                    "location",
                    "start_date",
                    "end_date",
                    "details",
                ],
                "additionalProperties": False,
            },
        },

        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "job_title": {
                        "type": "string"
                    },
                    "company": {
                        "type": "string"
                    },
                    "location": {
                        "type": ["string", "null"]
                    },
                    "start_date": {
                        "type": ["string", "null"]
                    },
                    "end_date": {
                        "type": ["string", "null"]
                    },
                    "description": {
                        "type": "string"
                    },
                },
                "required": [
                    "job_title",
                    "company",
                    "location",
                    "start_date",
                    "end_date",
                    "description",
                ],
                "additionalProperties": False,
            },
        },

        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "technologies": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                    },
                },
                "required": [
                    "name",
                    "description",
                    "technologies",
                ],
                "additionalProperties": False,
            },
        },

        "certifications": {
            "type": "array",
            "items": {
                "type": "string"
            },
        },

        "achievements": {
            "type": "array",
            "items": {
                "type": "string"
            },
        },
    },

    "required": [
        "contact",
        "summary",
        "skills",
        "education",
        "experience",
        "projects",
        "certifications",
        "achievements",
    ],

    "additionalProperties": False,
}


# ============================================================
# GROQ PARSER
# ============================================================

class GroqResumeParser:

    def __init__(self):

        if not GROQ_API_KEY:
            raise GroqParserError(
                "GROQ_API_KEY is not configured."
            )

        try:
            self.client = Groq(
                api_key=GROQ_API_KEY
            )
        except Exception as error:
            raise GroqParserError(
                "Failed to initialize Groq client."
            ) from error

        self.model = GROQ_MODEL

    # ========================================================
    # PARSE RESUME
    # ========================================================

    def parse(
        self,
        resume_text: str,
    ) -> dict[str, Any]:

        if not resume_text or not resume_text.strip():
            raise GroqParserError(
                "Resume text cannot be empty."
            )

        system_prompt = """
You are an expert resume information extraction system.

Your task is to extract structured information from
the provided resume text.

Rules:

1. Extract only information explicitly present in the resume.
2. Never invent missing information.
3. If a field is not present, return null.
4. Preserve the meaning of the original resume.
5. Keep skills as concise skill names.
6. Keep project technologies as technologies explicitly
   mentioned for that project.
7. Keep experience descriptions faithful to the resume.
8. Do not infer job titles, companies, dates, or degrees.
9. Return the information according to the provided JSON schema.
"""

        user_prompt = f"""
Extract structured resume information from this resume:

---------------- RESUME ----------------

{resume_text}

-------------- END RESUME --------------
"""

        try:

            response = (
                self.client.chat.completions.create(
                    model=self.model,

                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],

                    temperature=0,

                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "resume_profile",
                            "strict": True,
                            "schema": RESUME_SCHEMA,
                        },
                    },
                )
            )

        except Exception as error:

            raise GroqParserError(
                f"Groq API request failed: {error}"
            ) from error

        try:

            content = (
                response
                .choices[0]
                .message
                .content
            )

            if not content:
                raise GroqParserError(
                    "Groq returned an empty response."
                )

            parsed_data = json.loads(
                content
            )

        except json.JSONDecodeError as error:

            raise GroqParserError(
                "Groq returned invalid JSON."
            ) from error

        except Exception as error:

            if isinstance(
                error,
                GroqParserError,
            ):
                raise

            raise GroqParserError(
                "Failed to read Groq response."
            ) from error

        return parsed_data


# ============================================================
# CONVENIENCE FUNCTION
# ============================================================

def parse_resume_with_groq(
    resume_text: str,
) -> dict[str, Any]:

    parser = GroqResumeParser()

    return parser.parse(
        resume_text
    )