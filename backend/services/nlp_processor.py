import re

from backend.core.config import SPACY_MODEL


class NLPProcessorError(Exception):
    """Base exception for NLP processing errors."""


class NLPProcessor:
    """
    Memory-optimized spaCy NLP processor.

    spaCy itself and the NLP model are loaded lazily.
    This keeps FastAPI startup lightweight.
    """

    def __init__(self):
        self.nlp = None

    def _get_nlp(self):
        """
        Lazily load spaCy and the configured language model.

        The model is loaded only when resume processing is requested.
        """

        if self.nlp is None:
            try:
                import spacy

                self.nlp = spacy.load(
                    SPACY_MODEL,
                    disable=["tagger", "attribute_ruler", "lemmatizer"],
                )

            except OSError as error:
                raise NLPProcessorError(
                    f"spaCy model '{SPACY_MODEL}' is not installed."
                ) from error

            except Exception as error:
                raise NLPProcessorError(
                    "Failed to load spaCy NLP model."
                ) from error

        return self.nlp

    def clean_text(self, text: str) -> str:
        """Clean extracted resume text."""

        if not text:
            return ""

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Normalize spaces inside lines
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def detect_sections(self, text: str) -> dict:
        """
        Detect common resume sections.

        Returns section name -> section content.
        """

        section_patterns = {
            "summary": r"^(summary|professional summary|profile|objective|career objective)$",
            "skills": r"^(skills|technical skills|core skills|key skills|skills & technologies)$",
            "education": r"^(education|academic background|educational background)$",
            "experience": r"^(experience|work experience|professional experience|internship|internships)$",
            "projects": r"^(projects|academic projects|personal projects|key projects)$",
            "certifications": r"^(certifications|certificates)$",
            "achievements": r"^(achievements|accomplishments)$",
            "hobbies": r"^(hobbies|interests|interests & hobbies)$",
        }

        sections = {}
        current_section = None
        current_content = []

        lines = text.split("\n")

        for line in lines:
            cleaned_line = line.strip()

            if not cleaned_line:
                continue

            normalized_line = cleaned_line.lower()

            # Remove common decorative characters
            normalized_line = re.sub(
                r"^[•❖▪●\-–—\s]+",
                "",
                normalized_line,
            )

            matched_section = None

            for section_name, pattern in section_patterns.items():
                if re.match(pattern, normalized_line):
                    matched_section = section_name
                    break

            if matched_section:
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(
                        current_content
                    ).strip()

                current_section = matched_section
                current_content = []

            elif current_section:
                current_content.append(cleaned_line)

        # Save final section
        if current_section:
            sections[current_section] = "\n".join(
                current_content
            ).strip()

        return sections

    def process(self, text: str) -> dict:
        """Process resume text using spaCy."""

        if not text or not text.strip():
            raise NLPProcessorError(
                "Resume text cannot be empty."
            )

        cleaned_text = self.clean_text(text)

        nlp = self._get_nlp()

        doc = nlp(cleaned_text)

        tokens = [
            token.text
            for token in doc
            if not token.is_space
        ]

        sentences = [
            sentence.text.strip()
            for sentence in doc.sents
            if sentence.text.strip()
        ]

        entities = [
            {
                "text": entity.text,
                "label": entity.label_,
            }
            for entity in doc.ents
        ]

        sections = self.detect_sections(cleaned_text)

        return {
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "sentences": sentences,
            "entities": entities,
            "sections": sections,
            "token_count": len(tokens),
            "sentence_count": len(sentences),
        }


# One shared processor instance.
# The actual spaCy model remains lazy-loaded.
_default_processor = NLPProcessor()


def process_resume_text(text: str) -> dict:
    """
    Convenience function for processing resume text.

    Reuses one NLPProcessor instead of creating a new
    processor/model for every request.
    """

    return _default_processor.process(text)