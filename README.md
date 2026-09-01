# AI Technical Interviewer & Remediation Platform

Pure Python, Streamlit-based interview platform featuring dynamic Llama 3 question generation, OpenAI Whisper speech transcription, parallel multi-agent evaluation, dynamic remediation quiz gates, and visual delta tracking charts.

## Setup Instructions

1. **Install Prerequisites**:
   - Install [Ollama](https://ollama.ai/) and run Llama 3:
     ```bash
     ollama pull llama3
     ```
   - Install FFmpeg (required for Whisper audio processing).

2. **Install Python Dependencies**:
   ```bash
   pip install streamlit langchain langchain-community openai-whisper matplotlib numpy
