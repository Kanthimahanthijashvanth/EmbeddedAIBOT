from pathlib import Path
class SlideStructureBuilder:

    def __init__(
        self,
        file_path,
        slides,
        tables=None,
        images=None
    ):
        self.file_path = Path(file_path)
        self.slides = slides
        self.tables = tables or []
        self.images = images or []

    def build(self):

        structured_slides = []

        for slide in self.slides:

            slide_number = slide["slide_number"]
            text_items = []
            code_items = []

            for item in slide["text"]:

                content_type = item.get(
                    "content_type",
                    "text"
                )

                if content_type == "code":
                    code_items.append(item)

                else:
                    text_items.append(item)

            slide_tables = [
                table
                for table in self.tables
                if table["slide_number"] == slide_number
            ]


            slide_images = [
                image
                for image in self.images
                if image["slide_number"] == slide_number
            ]

            structured_slide = {
                "slide_number": slide_number,

                "source": str(
                    self.file_path
                ),

                "file_name": self.file_path.name,

                "workshop_id": self.file_path.stem,

                "content": {
                    "text": text_items,
                    "code": code_items,
                    "tables": slide_tables,
                    "images": slide_images
                }
            }

            structured_slides.append(
                structured_slide
            )

        return structured_slides