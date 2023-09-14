# Use the official Alpine Linux as the base image
FROM alpine:latest

# Set environment variables to ensure Python outputs everything to the console
ENV PYTHONUNBUFFERED 1

# Install system dependencies, Python, FLAC, and required Python packages
RUN apk --no-cache add \
    python3 \
    py3-pip \
    flac \
    libogg \
    libvorbis \
    file

# Set the working directory in the container
WORKDIR /app

# Copy the Python script (flac_checker.py) into the container
COPY flac_checker.py /app/

# Command to run the Python script
CMD ["python3", "flac_checker.py"]