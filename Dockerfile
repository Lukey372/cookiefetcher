# Use official Python image
FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    curl \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libgbm1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome.deb || apt-get -fy install \
    && rm google-chrome.deb

# Download and install Chromedriver properly
RUN wget -q -O chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver.zip \
    && chmod +x chromedriver \
    && mv chromedriver /usr/local/bin/chromedriver \
    && rm chromedriver.zip

# Start Flask API
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.server:app"]
