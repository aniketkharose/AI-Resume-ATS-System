import re


# ============================================================
# DOMAIN-AWARE SKILL DATABASE
# ============================================================

SKILL_DATABASE = {

    "Programming Languages": {
        "Python": ["python"],
        "C": ["c"],
        "C++": ["c++", "cpp"],
        "Java": ["java"],
        "JavaScript": ["javascript", "js"],
        "TypeScript": ["typescript", "ts"],
    },

    "AI / Machine Learning": {
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning", "dl"],
        "NumPy": ["numpy"],
        "Pandas": ["pandas"],
        "Matplotlib": ["matplotlib"],
        "Scikit-learn": ["scikit-learn", "scikit -learn", "sklearn"],
        "NLP": ["nlp", "natural language processing"],
        "Transformers": ["transformers", "transformer"],
        "LLMs": ["llm", "llms", "large language models"],
        "Generative AI": ["generative ai", "gen ai"],
        "RAG": ["rag", "retrieval augmented generation"],
        "PyTorch": ["pytorch"],
        "TensorFlow": ["tensorflow"],
        "Keras": ["keras"],
        "Computer Vision": ["computer vision"],
        "CNN": ["cnn", "convolutional neural network"],
        "RNN": ["rnn", "recurrent neural network"],
        "SVM": ["svm", "support vector machine"],
        "Decision Trees": ["decision tree", "decision trees"],
        "Naive Bayes": ["naive bayes"],
    },

    "Software Development": {
        "HTML": ["html"],
        "CSS": ["css"],
        "React": ["react", "react.js", "reactjs"],
        "FastAPI": ["fastapi", "fast api"],
        "Flask": ["flask"],
        "Django": ["django"],
        "REST APIs": ["rest api", "rest apis"],
        "Streamlit": ["streamlit"],
        "OpenCV": ["opencv", "open cv"],
        "Git": ["git"],
        "GitHub": ["github"],
        "VS Code": ["vs code", "visual studio code"],
    },

    "Embedded Systems": {
        "Embedded C": ["embedded c"],
        "Embedded Systems": ["embedded systems"],
        "Microcontrollers": ["microcontroller", "microcontrollers"],
        "8051": ["8051"],
        "PIC": ["pic", "pic18f4550"],
        "ARM": ["arm", "arm cortex", "cortex-m"],
        "STM32": ["stm32"],
        "ESP32": ["esp32"],
        "ESP8266": ["esp8266"],
        "Arduino": ["arduino"],
        "Raspberry Pi": ["raspberry pi"],
        "FreeRTOS": ["freertos", "free rtos"],
        "Keil": ["keil", "keil uvision"],
        "RTOS": ["rtos", "real time operating system"],
    },

    "Electronics / ENTC": {
        "Digital Electronics": ["digital electronics"],
        "Analog Electronics": ["analog electronics"],
        "Digital Signal Processing": [
            "digital signal processing",
            "dsp",
        ],
        "PCB Design": ["pcb design"],
        "VLSI": ["vlsi"],
        "Verilog": ["verilog"],
        "VHDL": ["vhdl"],
        "FPGA": ["fpga"],
        "MATLAB": ["matlab"],
        "Simulink": ["simulink"],
        "Signal Processing": ["signal processing"],
        "Electronic Circuits": ["electronic circuits"],
    },

    "IoT": {
        "IoT": ["iot", "internet of things"],
        "MQTT": ["mqtt"],
        "Sensors": ["sensor", "sensors"],
        "Wi-Fi": ["wi-fi", "wifi"],
        "Bluetooth": ["bluetooth"],
        "ThingSpeak": ["thingspeak"],
        "Node-RED": ["node-red", "nodered"],
        "IoT Protocols": ["iot protocols"],
    },

    "Communication": {
        "UART": ["uart"],
        "SPI": ["spi"],
        "I2C": ["i2c", "i²c"],
        "CAN": ["can protocol", "can bus", "controller area network"],
        "RF": ["rf", "radio frequency"],
        "Wireless Communication": ["wireless communication"],
        "GSM": ["gsm"],
        "GPS": ["gps"],
        "Bluetooth Communication": ["bluetooth communication"],
        "Zigbee": ["zigbee"],
        "LoRa": ["lora", "lora wan"],
        "TCP/IP": ["tcp/ip", "tcp ip"],
    },

    "Database": {
        "SQL": ["sql", "sq l"],
        "MySQL": ["mysql"],
        "PostgreSQL": ["postgresql", "postgres"],
        "SQLite": ["sqlite"],
        "MongoDB": ["mongodb", "mongo db"],
        "Supabase": ["supabase"],
        "Firebase": ["firebase"],
    },

    "Cloud / DevOps": {
        "AWS": ["aws", "amazon web services"],
        "Azure": ["azure"],
        "Google Cloud": ["google cloud", "gcp"],
        "Docker": ["docker"],
        "Linux": ["linux"],
        "GitHub Actions": ["github actions"],
        "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
    },

    "Tools": {
        "Keil": ["keil", "keil uvision"],
        "MATLAB": ["matlab"],
        "Simulink": ["simulink"],
        "Xilinx Vivado": ["vivado", "xilinx vivado"],
        "Proteus": ["proteus"],
        "Multisim": ["multisim"],
        "Arduino IDE": ["arduino ide"],
        "VS Code": ["vs code", "visual studio code"],
    },
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize extracted resume text so that common PDF
    extraction artifacts do not break skill matching.
    """

    if not text:
        return ""

    text = text.lower()

    replacements = {
        "sq l": "sql",
        "fast api": "fastapi",
        "scikit -learn": "scikit-learn",
        "scikit - learn": "scikit-learn",
        "free rtos": "freertos",
        "mongo db": "mongodb",
        "wi-fi": "wifi",
        "react.js": "react",
        "reactjs": "react",
        "open cv": "opencv",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SAFE SKILL MATCHING
# ============================================================

def skill_found(text: str, alias: str) -> bool:
    """
    Check whether a skill alias exists as a meaningful
    standalone term.

    This prevents accidental matches such as:
        C -> appearing inside "communication"
        Java -> appearing inside "JavaScript"
    """

    alias = normalize_text(alias)

    if not alias:
        return False

    escaped_alias = re.escape(alias)

    pattern = rf"(?<![a-z0-9+#]){escaped_alias}(?![a-z0-9+#])"

    return re.search(pattern, text) is not None


# ============================================================
# SECTION SOURCE DETECTION
# ============================================================

def get_section_source(sections: dict, skill_alias: str) -> tuple[str, str]:
    """
    Find the first section containing the skill.

    Returns:
        (section_name, evidence)
    """

    normalized_alias = normalize_text(skill_alias)

    # Prefer Skills section because it is the strongest
    # explicit indication of a candidate's skill.
    section_priority = [
        "skills",
        "experience",
        "projects",
        "education",
        "summary",
        "certifications",
        "achievements",
        "hobbies",
    ]

    for section_name in section_priority:

        section_text = sections.get(section_name, "")

        if not section_text:
            continue

        normalized_section = normalize_text(section_text)

        if skill_found(normalized_section, normalized_alias):

            # Find a useful sentence/line containing the skill.
            lines = section_text.split("\n")

            for line in lines:

                if skill_found(
                    normalize_text(line),
                    normalized_alias,
                ):
                    return section_name, line.strip()

            return section_name, section_text[:200].strip()

    return "resume", ""


# ============================================================
# SPECIAL HANDLING FOR AMBIGUOUS SHORT SKILLS
# ============================================================

def is_valid_short_skill(
    canonical_skill: str,
    sections: dict,
) -> bool:
    """
    Short terms can create false positives.

    Example:
        C
        ARM
        RF
        GPS
        CAN

    These are accepted only when there is stronger evidence.
    """

    short_skills = {
        "C",
        "ARM",
        "RF",
        "GPS",
        "CAN",
        "SPI",
        "I2C",
        "UART",
        "PIC",
    }

    if canonical_skill not in short_skills:
        return True

    # Skills explicitly listed in the Skills section
    # are stronger evidence.
    skills_section = normalize_text(
        sections.get("skills", "")
    )

    aliases = []

    for category_skills in SKILL_DATABASE.values():

        if canonical_skill in category_skills:
            aliases = category_skills[canonical_skill]
            break

    for alias in aliases:

        if skill_found(skills_section, alias):
            return True

    # Otherwise require the term to appear in another
    # technical section.
    technical_sections = [
        "experience",
        "projects",
        "education",
        "certifications",
    ]

    for section_name in technical_sections:

        section_text = normalize_text(
            sections.get(section_name, "")
        )

        for alias in aliases:

            if skill_found(section_text, alias):
                return True

    return False


# ============================================================
# MAIN SKILL EXTRACTION
# ============================================================

def extract_skills_from_sections(
    sections: dict,
) -> list[dict]:

    if not sections:
        return []

    detected_skills = []
    detected_names = set()

    for category, skills in SKILL_DATABASE.items():

        for canonical_skill, aliases in skills.items():

            # Check all aliases
            matched_alias = None

            for alias in aliases:

                # Search across all sections
                for section_name, section_text in sections.items():

                    normalized_section = normalize_text(
                        section_text
                    )

                    normalized_alias = normalize_text(
                        alias
                    )

                    if skill_found(
                        normalized_section,
                        normalized_alias,
                    ):
                        matched_alias = alias
                        break

                if matched_alias:
                    break

            if not matched_alias:
                continue

            # Protect against short/common false positives
            if not is_valid_short_skill(
                canonical_skill,
                sections,
            ):
                continue

            # Prevent duplicate skills
            if canonical_skill in detected_names:
                continue

            source, evidence = get_section_source(
                sections,
                matched_alias,
            )

            detected_skills.append(
                {
                    "skill": canonical_skill,
                    "category": category,
                    "source": source,
                    "evidence": evidence,
                }
            )

            detected_names.add(canonical_skill)

    return detected_skills


# ============================================================
# OPTIONAL: SIMPLE SKILL LIST
# ============================================================

def get_skill_names(
    skills: list[dict],
) -> list[str]:
    """
    Convert detailed skill objects into a simple list.

    Useful later for ATS matching.
    """

    return [
        item["skill"]
        for item in skills
    ]