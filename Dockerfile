 # Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the contents of your project into the /app directory in the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (optional, for HTTP bots)
EXPOSE 5000

# Set the default command to run your bot
CMD ["python", "index.py"]
