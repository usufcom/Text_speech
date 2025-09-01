# PDF to Audiobook Converter

A Python-based tool that converts PDF documents into high-quality audiobooks using OpenAI's Text-to-Speech (TTS) API.

## Features

- **PDF to Audio Conversion**: Convert PDF documents into professional audiobooks
- **Multiple Voice Styles**: Choose from 6 different voice personalities
- **Customizable Chunking**: Control text processing size for optimal performance
- **Professional Instructions**: Add custom reading instructions for better audio quality
- **Jupyter Notebook Support**: Easy-to-use examples and testing

## Voice Styles Available

- **alloy** - Neutral, natural voice
- **verse** - Softer, storytelling voice
- **aria** - Warmer, expressive voice
- **sage** - Calm, thoughtful voice
- **lumen** - Bright, youthful voice
- **echo** - Clear, neutral, slightly robotic voice

## Installation

1. Clone the repository:
```bash
git clone https://github.com/usufcom/Text_speech
cd Text-speech
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key inside the `.env` file: `OPENAI_API_KEY=your_api_key_here`

## Usage

### Basic Usage

```python
from PDF2Audio import PDFToAudiobook

# Initialize the converter
converter = PDFToAudiobook(
    chunk_size=1500,  # Tokens per chunk
    voice="verse",    # Voice style
    instructions="Read in a calm and professional audiobook style."
)

# Convert your PDF
pdf_file = "path/to/your/document.pdf"
converter.convert_pdf(pdf_file)
```

### Jupyter Notebook Example

See `Example_usage.ipynb` for a complete working example.

## Configuration Options

- **chunk_size**: Number of tokens to process at once (default: 1500)
- **voice**: Voice style to use (default: "verse")
- **instructions**: Custom reading instructions for the AI

## Project Structure

```
Text-speech/
├── PDF2Audio.py              # Main conversion module
├── Example_usage.ipynb       # Usage examples
├── Test_text2speech.ipynb    # Testing notebook
├── docs/                     # Documentation and sample PDFs
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

## Requirements

- Python 3.7+
- OpenAI API key
- Required Python packages (see requirements.txt)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool uses OpenAI's API and may incur costs based on your usage. Please review OpenAI's pricing and terms of service before use.

## Support
If you have any questions or need help, please reach out:

Website: www.djamai.com
Email: usufcom20@gmail.com
LinkedIn: @usufcom

For issues and questions, please open an issue on the GitHub repository.
