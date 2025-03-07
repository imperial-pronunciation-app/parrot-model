# Parrot-Model

## 📖 Overview
Parrot-Model is a component of the Parrot language learning platform, focusing on pronunciation assessment and feedback. It leverages speech recognition models to analyze user pronunciations and provide detailed insights to enhance language learning.

## 📂 Project Structure
```
.
├── app/                    # Main application logic
│   ├── main.py             # FastAPI application entry point
│   ├── routers/            # API route handlers
│   ├── schemas/            # Request/response models
│   ├── services/           # Audio processing & inference
│   └── utils/              # Utility functions
├── config/                 # Configuration settings
├── tests/                  # Unit and integration tests
├── Dockerfile              # Docker image specification
├── docker-compose.yml      # Docker Compose setup
├── Makefile                # Makefile for common tasks
├── requirements.txt        # Python dependencies
├── deploy.sh               # Deployment script
└── README.md               # Project documentation
```

## 🚀 Getting Started

### Running the Application
#### Using Docker (Recommended)
```sh
make dev
```

### Running Tests
To execute tests using Docker:
```sh
make test
```

## 🛠 Development

### Formatting & Linting
```sh
pre-commit run --all-files
```

## 📚 Acknowledgements
This project utilizes the following open-source technologies:

- **OpenAI's Whisper**: A state-of-the-art speech recognition system developed by OpenAI, capable of transcribing speech in multiple languages and translating non-English languages into English. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Whisper_%28speech_recognition_system%29?utm_source=chatgpt.com))

- **Allosaurus**: An open-source phonemic transcription tool that provides detailed phonemic transcriptions across various languages, aiding in precise pronunciation analysis. (github.com/pyllosaurus/allosaurus)
