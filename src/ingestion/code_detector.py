import re


class CodeDetector:

    CODE_PATTERNS = [

        # Python
        r"\bdef\s+\w+\s*\(",
        r"\bimport\s+\w+",
        r"\bfrom\s+\w+\s+import\s+",
        r"\bprint\s*\(",

        # C / C++
        r"#include\s*[<\"]",
        r"\bint\s+main\s*\(",
        r"\bvoid\s+\w+\s*\(",
        r"\bprintf\s*\(",
        r"\bscanf\s*\(",

        # Java
        r"\bpublic\s+class\s+\w+",
        r"\bpublic\s+static\s+void\s+main",

        # JavaScript
        r"\bconsole\.log\s*\(",
        r"\bfunction\s+\w+\s*\(",

        # Common programming syntax
        r"\bif\s*\(.+\)\s*\{",
        r"\bfor\s*\(.+\)\s*\{",
        r"\bwhile\s*\(.+\)\s*\{",
        r"==",
        r"!=",
        r"&&",
        r"\|\|",
    ]

    def __init__(self):
        self.patterns = [
            re.compile(pattern)
            for pattern in self.CODE_PATTERNS
        ]

    def is_code(self, text):

        if not text or not text.strip():
            return False

        matches = 0

        for pattern in self.patterns:

            if pattern.search(text):
                matches += 1

        return matches >= 1

    def detect(self, slides):

        for slide in slides:

            for item in slide["text"]:

                text = item["content"]

                item["content_type"] = (
                    "code"
                    if self.is_code(text)
                    else "text"
                )

        return slides