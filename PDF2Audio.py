import os
import re
from pathlib import Path
import fitz  # PyMuPDF
import tiktoken
from openai import OpenAI


class PDFToAudiobook:
    def __init__(
        self,
        api_key=None,
        chunk_size=1800,
        voice="verse",
        instructions="Read in a calm, clear, and engaging tone, like a professional audiobook narrator."
    ):
        """
        Initialize the PDFToAudiobook converter.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.chunk_size = chunk_size
        self.voice = voice
        self.instructions = instructions
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def pdf_to_text(self, pdf_path):
        """Extract clean text from PDF, removing headers/footers."""
        doc = fitz.open(pdf_path)
        all_text = []

        for page in doc:
            text = page.get_text("text")
            # Remove headers/footers heuristically (first and last 2 lines)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if len(lines) > 4:
                lines = lines[2:-2]
            page_text = "\n".join(lines)
            all_text.append(page_text)

        return "\n".join(all_text)

    def split_into_chapters(self, text):
        """Split text into chapters/sections using headings."""
        chapters = []
        current_title = "Intro"
        current_content = []

        for line in text.splitlines():
            # Heuristic: lines in ALL CAPS or starting with 'Chapter'
            if re.match(r'^(CHAPTER|Chapter|SECTION|Section)\b', line) or line.isupper():
                if current_content:
                    chapters.append((current_title, "\n".join(current_content)))
                    current_content = []
                current_title = line.strip()[:50]  # limit length for filename
            else:
                current_content.append(line)

        if current_content:
            chapters.append((current_title, "\n".join(current_content)))

        return chapters

    def chunk_text(self, text):
        """Split text into chunks < chunk_size tokens."""
        tokens = self.encoder.encode(text)
        chunks = []
        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_text = self.encoder.decode(tokens[start:end])
            chunks.append(chunk_text)
            start += self.chunk_size
        return chunks

    def text_to_speech(self, text, output_file):
        """Convert text to speech and save as MP3."""
        with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=self.voice,
            input=text,
            instructions=self.instructions
        ) as response:
            response.stream_to_file(output_file)

    def convert_pdf(self, pdf_path):
        """Main function to convert PDF to audiobook (multiple MP3s)."""
        pdf_path = Path(pdf_path)
        pdf_name = pdf_path.stem

        # Create output folder
        output_dir = pdf_path.parent / f"{pdf_name}_audiobook"
        output_dir.mkdir(exist_ok=True)

        print(f"📖 Extracting text from {pdf_path} ...")
        text = self.pdf_to_text(pdf_path)

        print("📑 Splitting text into chapters/sections ...")
        chapters = self.split_into_chapters(text)

        for idx, (title, content) in enumerate(chapters):
            tts_chunks = self.chunk_text(content)
            for c_idx, chunk in enumerate(tts_chunks):
                safe_title = re.sub(r'\W+', '_', title)
                audio_file = output_dir / f"{pdf_name}_{idx}_{c_idx}_{safe_title}.mp3"
                print(f"🎙️ Generating audio: {audio_file}")
                self.text_to_speech(chunk, audio_file)

        print(f"✅ Audiobook created in folder: {output_dir}")


# --- Example usage ---
if __name__ == "__main__":
    pdf_file = "Executive_summary_GDPR.pdf"  # Replace with your PDF filename
    converter = PDFToAudiobook(
        chunk_size=1500,  # Tokens per chunk
        voice="verse",    # Voice style
        instructions="Read in a calm and professional audiobook style."
    )
    converter.convert_pdf(pdf_file)
