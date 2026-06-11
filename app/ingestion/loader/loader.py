import os
import cv2
from pathlib import Path
from PIL import Image
import pytesseract
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import (
    WebBaseLoader, 
    PyPDFLoader, 
    TextLoader, 
    CSVLoader
)
from langchain_core.documents import Document

# Load environment variables


# Configure Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class DocumentLoader:
    """A centralized utility class to ingest multiple media types into LangChain Documents."""
    
    @staticmethod
    def load_video_text(file_path: Path, frame_interval: int = 30) -> list[Document]:
        """Extracts unique lines of text found on-screen across video frames."""
        video = cv2.VideoCapture(str(file_path))
        if not video.isOpened():
            print(f"Warning: Cannot open video file {file_path}")
            return []

        unique_lines = set()
        frame_count = 0
        
        while True:
            success, frame = video.read()
            if not success:
                break
                
            if frame_count % frame_interval == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_frame)
                text = pytesseract.image_to_string(pil_img)
                
                for line in text.split('\n'):
                    clean_line = line.strip()
                    if len(clean_line) > 5:
                        unique_lines.add(clean_line)
            frame_count += 1

        video.release()
        
        combined_text = "\n".join(unique_lines)
        return [Document(page_content=combined_text, metadata={"source": str(file_path), "type": "video"})]

    @staticmethod
    def load_image_text(file_path: Path) -> list[Document]:
        """Extracts text from a single static image via OCR."""
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            return [Document(page_content=text, metadata={"source": str(file_path), "type": "image"})]
        except Exception as e:
            print(f"Error processing image {file_path}: {e}")
            return []

    @classmethod
    def load_directory(cls, directory_path: str) -> list[Document]:
        """Scans a directory and accurately loads files based on their extensions."""
        all_documents = []
        
        # Standard Loader Mapping
        standard_loaders = {
            ".pdf": PyPDFLoader,
            ".txt": TextLoader,
            ".csv": CSVLoader,
        }

        for file in Path(directory_path).glob("*"):
            if file.is_dir():
                continue
                
            suffix = file.suffix.lower()

            # Handle standard text/data documents
            if suffix in standard_loaders:
                try:
                    loader_class = standard_loaders[suffix]
                    loader = loader_class(str(file))
                    all_documents.extend(loader.load())
                except Exception as e:
                    print(f"Error loading {file.name}: {e}")
                    
            # Handle Video OCR
            elif suffix in [".mp4", ".avi", ".mov"]:
                all_documents.extend(cls.load_video_text(file, frame_interval=30))
                
            # Handle Image OCR
            elif suffix in [".png", ".jpg", ".jpeg", ".tiff"]:
                all_documents.extend(cls.load_image_text(file))
                
            else:
                print(f"Unsupported file type skipped: {file.name}")

        return all_documents






