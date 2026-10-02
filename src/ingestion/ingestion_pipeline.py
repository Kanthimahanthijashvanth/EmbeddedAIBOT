from pathlib import Path

from src.ingestion.loader import WorkshopLoader
from src.ingestion.slide_parser import SlideParser
from src.ingestion.code_detector import CodeDetector
from src.ingestion.table_extractor import TableExtractor
from src.ingestion.slide_structure import SlideStructureBuilder


class WorkshopIngestionPipeline:

    def __init__(self, data_dir="Data"):

        self.data_dir = Path(data_dir)

        self.code_detector = CodeDetector()

    def process_file(self, file_path):

        file_path = Path(file_path)

        loader = WorkshopLoader(file_path)

        # Load basic documents
        documents = loader.load()

        # PDF
        if file_path.suffix.lower() == ".pdf":
            return {
                "file": str(file_path),
                "documents": documents
            }

        # PPTX
        parser = SlideParser(file_path)
        slides = parser.parse()

        slides = self.code_detector.detect(slides)

        table_extractor = TableExtractor(file_path)
        tables = table_extractor.extract()

        structure_builder = SlideStructureBuilder(
            file_path=file_path,
            slides=slides,
            tables=tables,
            images=[]
        )

        structured_slides = structure_builder.build()

        return {
            "file": str(file_path),
            "documents": documents,
            "slides": structured_slides
        }

    def process_all(self):

        files = []

        for extension in ["*.pptx", "*.pdf"]:

            files.extend(
                self.data_dir.glob(extension)
            )

        results = []

        for file_path in files:

            result = self.process_file(
                file_path
            )

            results.append(result)

        return results