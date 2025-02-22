# Use official Python image
FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# ✅ Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    jq \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libgbm1 \
    libgtk-3-0 \
    fonts-liberation \
    libvulkan1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# ✅ Install Latest Google Chrome
RUN wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome.deb \
    && rm google-chrome.deb

# ✅ Ensure Chrome is Installed Correctly
RUN google-chrome --version

# ✅ Install the Correct Version of ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROMEDRIVER_VERSION=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json | jq -r --arg VER "$CHROME_VERSION" '.versions[] | select(.version==$VER) | .downloads.chromedriver[] | select(.platform == "linux64").url' | head -n 1) \
    && wget -q -O chromedriver.zip "$CHROMEDRIVER_VERSION" \
    && unzip chromedriver.zip \
    && chmod +x chromedriver \
    && mv chromedriver /usr/local/bin/chromedriver \
    && rm chromedriver.zip

# ✅ Ensure ChromeDriver is Installed Correctly
RUN chromedriver --version

# Start Flask API
COPY . .
CMD exec gunicorn -b 0.0.0.0:5000 app.server:app --workers=1 --threads=2 --timeout 120 --log-level debug
