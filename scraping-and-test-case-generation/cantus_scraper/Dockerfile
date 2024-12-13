# Use an official Python image as a base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the scraping and processing scripts into the container
COPY scraper.py .
COPY process_csvs.py .

# Install Python dependencies
RUN pip install --no-cache-dir requests beautifulsoup4

# Ensure the required directory for valid CSVs is created
RUN mkdir -p /app/validCSVs

# Command to run the scraping and processing scripts
CMD ["bash", "-c", "python scraper.py && python process_csvs.py"]
