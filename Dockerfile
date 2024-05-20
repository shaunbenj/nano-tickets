# Base image with Python 3
FROM python:3.12.3

# Define environment variables
ENV APP_PATH=/app
ENV PORT=80

# Create working directory
WORKDIR $APP_PATH

# Install dependencies
COPY requirements.txt $APP_PATH/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port for the app
EXPOSE $PORT

# Command to run the app
CMD ["python", "-u", "index.py"] 