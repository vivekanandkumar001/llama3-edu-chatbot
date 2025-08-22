# LLaMA3 Hybrid RAG EduBot (local, Python)

Quick start (Windows):

1. Install Ollama (https://ollama.com/download) and restart PC.
2. Open project folder in VS Code.
3. Create & activate venv:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
4. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
5. Download the model:
    ```bash
    ollama pull llama3:hybrid-rag-educational
    ```
6. Run the bot:
    ```bash
    python bot.py
    ```
7. Open the browser and go to `http://localhost:8000` to interact with the bot.
# LLaMA3 Hybrid RAG EduBot
This is a simple educational chatbot using LLaMA3 Hybrid RAG model. It can answer questions based on the provided educational materials.
# Features
- Uses LLaMA3 Hybrid RAG model for question answering.
- Supports local deployment with Ollama.
- Easy to set up and run on Windows.
# Requirements
- Python 3.8 or higher
- Ollama installed
- Basic knowledge of Python and virtual environments
# Usage
1. Follow the quick start instructions to set up the environment.
2. Place your educational materials in the `data` folder.
3. Run the bot using the provided command.
4. Interact with the bot through the web interface.
# Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or
improvements.
# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details