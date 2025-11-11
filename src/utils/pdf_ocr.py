"""
PDF OCR Utility Module
Extracts text from PDF files using OCR (Optical Character Recognition)
Supports both text-based PDFs and scanned image PDFs
"""

import io
import os
from typing import Any, Dict

try:
    import PyPDF2
    import pytesseract
    from pdf2image import convert_from_bytes, convert_from_path

    OCR_AVAILABLE = True
except ImportError as e:
    OCR_AVAILABLE = False
    print(f"Warning: OCR dependencies not available: {e}")


class PDFOCRExtractor:
    """Extract text from PDF files using OCR and text extraction"""

    def __init__(self):
        """Initialize PDF OCR Extractor"""
        if not OCR_AVAILABLE:
            raise ImportError(
                "OCR dependencies not installed. Run: pip install pytesseract pdf2image PyPDF2 pillow"
            )

        # Configure tesseract path for macOS (Homebrew installation)
        if os.path.exists("/opt/homebrew/bin/tesseract"):
            pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
        elif os.path.exists("/usr/local/bin/tesseract"):
            pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text from PDF using both text extraction and OCR

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with extracted text, page count, and metadata
        """
        result = {
            "text": "",
            "pages": [],
            "page_count": 0,
            "method": "unknown",
            "has_text": False,
            "has_images": False,
            "error": None,
        }

        try:
            # First try to extract text directly (for text-based PDFs)
            text_extracted = self._extract_text_direct(pdf_path)

            if text_extracted["text"].strip():
                result.update(text_extracted)
                result["method"] = "text_extraction"
                result["has_text"] = True
            else:
                # If no text found, use OCR (for scanned/image PDFs)
                ocr_extracted = self._extract_text_ocr(pdf_path)
                result.update(ocr_extracted)
                result["method"] = "ocr"
                result["has_images"] = True

        except Exception as e:
            result["error"] = str(e)

        return result

    def _extract_text_direct(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text directly from PDF (for text-based PDFs)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with extracted text and page information
        """
        result = {"text": "", "pages": [], "page_count": 0}

        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                result["page_count"] = len(pdf_reader.pages)

                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    result["pages"].append(
                        {
                            "page_number": page_num,
                            "text": page_text,
                            "char_count": len(page_text),
                        }
                    )
                    result["text"] += f"\n--- Page {page_num} ---\n{page_text}\n"

        except Exception as e:
            print(f"Error in direct text extraction: {e}")

        return result

    def _extract_text_ocr(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text using OCR (for scanned/image PDFs)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with OCR-extracted text and page information
        """
        result = {"text": "", "pages": [], "page_count": 0}

        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=300)
            result["page_count"] = len(images)

            for page_num, image in enumerate(images, 1):
                # Perform OCR on the image
                page_text = pytesseract.image_to_string(image)

                result["pages"].append(
                    {
                        "page_number": page_num,
                        "text": page_text,
                        "char_count": len(page_text),
                    }
                )
                result["text"] += f"\n--- Page {page_num} (OCR) ---\n{page_text}\n"

        except Exception as e:
            print(f"Error in OCR extraction: {e}")

        return result

    def extract_from_bytes(self, pdf_bytes: bytes) -> Dict[str, any]:
        """
        Extract text from PDF bytes (for uploaded files)

        Args:
            pdf_bytes: PDF file content as bytes

        Returns:
            Dictionary with extracted text, page count, and metadata
        """
        result = {
            "text": "",
            "pages": [],
            "page_count": 0,
            "method": "unknown",
            "error": None,
        }

        try:
            # Try direct text extraction first
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            result["page_count"] = len(pdf_reader.pages)

            text_content = ""
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                text_content += page_text
                result["pages"].append(
                    {
                        "page_number": page_num,
                        "text": page_text,
                        "char_count": len(page_text),
                    }
                )

            if text_content.strip():
                result["text"] = text_content
                result["method"] = "text_extraction"
            else:
                # Use OCR for scanned PDFs
                images = convert_from_bytes(pdf_bytes, dpi=300)
                result["page_count"] = len(images)
                result["pages"] = []

                ocr_text = ""
                for page_num, image in enumerate(images, 1):
                    page_text = pytesseract.image_to_string(image)
                    ocr_text += f"\n--- Page {page_num} (OCR) ---\n{page_text}\n"
                    result["pages"].append(
                        {
                            "page_number": page_num,
                            "text": page_text,
                            "char_count": len(page_text),
                        }
                    )

                result["text"] = ocr_text
                result["method"] = "ocr"

        except Exception as e:
            result["error"] = str(e)

        return result

    def get_pdf_info(self, pdf_path: str) -> Dict[str, any]:
        """
        Get PDF metadata and information

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with PDF metadata
        """
        info = {
            "filename": os.path.basename(pdf_path),
            "size_bytes": 0,
            "page_count": 0,
            "has_text": False,
            "metadata": {},
        }

        try:
            info["size_bytes"] = os.path.getsize(pdf_path)

            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                info["page_count"] = len(pdf_reader.pages)

                if pdf_reader.metadata:
                    info["metadata"] = {
                        "title": pdf_reader.metadata.get("/Title", ""),
                        "author": pdf_reader.metadata.get("/Author", ""),
                        "subject": pdf_reader.metadata.get("/Subject", ""),
                        "creator": pdf_reader.metadata.get("/Creator", ""),
                    }

                # Check if PDF has extractable text
                first_page_text = pdf_reader.pages[0].extract_text()
                info["has_text"] = bool(first_page_text.strip())

        except Exception as e:
            info["error"] = str(e)

        return info


def extract_pdf_text(pdf_path: str) -> str:
    """
    Simple function to extract text from PDF

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text as string
    """
    extractor = PDFOCRExtractor()
    result = extractor.extract_text_from_pdf(pdf_path)
    return result.get("text", "")


def analyze_pdf_structure(pdf_path: str) -> Dict[str, any]:
    """
    Analyze PDF structure and content for AI insights

    Args:
        pdf_path: Path to PDF file

    Returns:
        Dictionary with structured analysis
    """
    extractor = PDFOCRExtractor()

    # Get basic info
    info = extractor.get_pdf_info(pdf_path)

    # Extract text
    extraction = extractor.extract_text_from_pdf(pdf_path)

    # Analyze content
    analysis = {
        "file_info": info,
        "extraction": {
            "method": extraction.get("method"),
            "page_count": extraction.get("page_count"),
            "total_characters": len(extraction.get("text", "")),
            "has_content": bool(extraction.get("text", "").strip()),
        },
        "content": extraction.get("text", ""),
        "pages": extraction.get("pages", []),
        "summary": {
            "is_scanned": extraction.get("method") == "ocr",
            "is_text_based": extraction.get("method") == "text_extraction",
            "readable": bool(extraction.get("text", "").strip()),
        },
    }

    return analysis
