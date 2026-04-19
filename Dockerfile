# Use official lightweight Python 3.10 image
FROM python:3.10-slim

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose port 8080
ENV PORT=8080
EXPOSE 8080

# Command to run the application using uvicorn
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
