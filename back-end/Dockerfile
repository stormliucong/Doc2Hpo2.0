# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
# RUN pip install --no-binary :all: nmslib



# Download and install the wheel
# RUN curl -o nmslib_metabrainz-2.1.3-cp312-cp312-macosx_10_9_universal2.whl "https://files.pythonhosted.org/packages/fc/61/da4f0cf59a45ed55d58d3f248ae74842f57c3b11fe2b0aa73f9c5c7069a7/nmslib_metabrainz-2.1.3-cp312-cp312-macosx_10_9_universal2.whl" && \
#     pip install nmslib_metabrainz-2.1.3-cp312-cp312-macosx_10_9_universal2.whl && \
#     rm nmslib_metabrainz-2.1.3-cp312-cp312-macosx_10_9_universal2.whl
# Copy requirements.txt and install dependencies
COPY requirements.txt .
# A hot fix. 2.10.1 or higher  (latest as of today: 2.11.1)
# RUN pip install --upgrade pybind11

# For some reason, it can only be installed on linux/x86_64 platform
# But it did work on my host machine M2 macbook pro, which is arm64
# But in the docker container, it failed to install
# so I have to create this dockerfile to install it on linux/x86_64 platform
RUN pip install nmslib-metabrainz
# RUN pip install --only-binary=:all: nmslib-metabrainz
# RUN pip install 'nmslib @ git+https://github.com/nmslib/nmslib.git#egg=nmslib&subdirectory=python_bindings'

RUN pip install scispacy
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code
# COPY . .
# Use Volume to mount the code from the host machine

# Expose the Flask default port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]