FROM python:3.12-slim

RUN apt-get update

# required for pytesseract
RUN apt-get -y install tesseract-ocr
# RUN apt-get -y install tesseract-ocr-all
# RUN apt-get -y install tesseract-ocr-jpn
# RUN apt-get -y install tesseract-ocr-Japanese
# RUN apt-get -y install tesserocr

# Download language data (jpn, jpn_vert, osd) from official tessdata repo
RUN apt-get -y install wget
RUN wget -O /usr/share/tesseract-ocr/5/tessdata/jpn.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/jpn.traineddata
RUN wget -O /usr/share/tesseract-ocr/5/tessdata/jpn_vert.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/jpn_vert.traineddata
RUN wget -O /usr/share/tesseract-ocr/5/tessdata/Japanese.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/jpn.traineddata
RUN wget -O /usr/share/tesseract-ocr/5/tessdata/Japanese_vert.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/jpn_vert.traineddata
RUN wget -O /usr/share/tesseract-ocr/5/tessdata/osd.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/osd.traineddata
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

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