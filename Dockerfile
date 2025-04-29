FROM python:3.12-slim

# required for pytesseract
RUN apt-get update && apt-get -y install tesseract-ocr 

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml ./

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi --no-cache

# Copy the rest of the application code
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]