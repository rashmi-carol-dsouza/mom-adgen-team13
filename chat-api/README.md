# Local Event Advert API

This project provides a local API for generating radio-style event advertisements with background music. It uses FastAPI for the web server, integrates with external text-to-speech and language models (LMNT and Mistral), and processes audio with pydub.

## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Development Commands](#development-commands)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

## Project Overview

This API generates a short, engaging radio advertisement for live music events. It:
- Accepts event details via a POST request.
- Uses a language model to generate advertisement text.
- Converts the generated text to speech with background music.
- Returns the generated MP3 file as the response.

## Directory Structure

```
.
├── event_advert.py          # FastAPI app containing API endpoints and business logic
├── Makefile                 # Commands to install dependencies, run the app, format, and lint code
├── .env                     # File to store sensitive environment variables (not committed)
└── data/                    # Directory for storing generated audio files and background music
    ├── background_music.mp3 # Background music file used in the advertisement
    ├── advert.mp3           # Generated advert file (output)
    └── tts_output.mp3       # Temporary file for TTS output
```

## Prerequisites

- **Python 3.10+** (tested on Python 3.10 or later)
- **Poetry** for dependency management  
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- Other dependencies as listed in the `pyproject.toml` (installed via Poetry)

## Configuration

This project requires API keys for LMNT and Mistral services. These should be stored in a `.env` file in the project root (this file is excluded from version control):

Create a file named `.env` and add the following:

```dotenv
# .env file
LMNT_API_KEY=your-lmnt-api-key
MISTRAL_API_KEY=your-mistral-api-key
```

Ensure you replace the placeholder values with your actual API keys. The API code loads these variables using `python-dotenv`.

## Installation

1. **Clone the Repository**  
   Clone the project repository to your local machine.

2. **Install Dependencies**  
Use Poetry to install dependencies:
```bash
make install
```
   This command runs `poetry install` and installs all required libraries.

## Running the API

Start the FastAPI server in development mode using Uvicorn:
```bash
make run
```
This command will start the API server (by default on `http://127.0.0.1:8000`) with automatic reloading.

## API Endpoints

- **GET /**  
  Returns a welcome message.
  
  **Example Response:**
  ```json
  {
    "message": "Welcome to the Event Advert API!"
  }
  ```

- **POST /generate-advert/**  
  Accepts event details as JSON and returns the generated MP3 advertisement.
  
  **Request Body Example:**
  ```json
  {
    "event": {
      "artist_name": "The Sample Band",
      "event_type": "concert",
      "venue_name": "Sample Arena",
      "city": "Berlin",
      "country": "Germany",
      "event_start_date": "May 10",
      "event_start_time": "8 PM",
      "genres": ["rock", "pop"]
    }
  }
  ```
  
  **Response:**  
  A file response (`advert.mp3`) with `audio/mpeg` content type.

## Development Commands

The provided Makefile includes several commands:

- **install:**  
  Install all project dependencies using Poetry.
```bash
  make install
  ```

- **run:**  
  Run the FastAPI server in development mode.
  ```bash
  make run
  ```

- **format:**  
  Format code using [Black](https://github.com/psf/black).
```bash
  make format
  ```

- **lint:**  
  Lint code using [flake8](https://flake8.pycqa.org/).
```bash
  make lint
  ```

## Troubleshooting

- **API Keys Not Loaded:**  
  Ensure that the `.env` file is present in the project root and that it contains the correct `LMNT_API_KEY` and `MISTRAL_API_KEY` values.

- **Logs:**  
  Application logs are saved to `logs/event_advert.log` with rotation and retention settings configured in Loguru.

- **Directory Permissions:**  
  Verify that the `data` directory exists and is writable by the application. The code will create it automatically if it doesn't exist.

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [Loguru Documentation](https://loguru.readthedocs.io/)

---

This README provides an overview of your local API for generating event advertisements. Adjust configuration values and dependencies as needed for your development setup.
