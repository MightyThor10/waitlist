# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /waitlist/Code

# Install pip and virtualenv
RUN python -m pip install --upgrade pip
RUN pip install virtualenv

# # Copy the requirements file into the container
# COPY requirements.txt .

# # Create a virtual environment and install the requirements
# RUN virtualenv venv
# RUN . venv/bin/activate && pip install -r requirements.txt
