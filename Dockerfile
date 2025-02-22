# Use official Python image
FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    xvfb \
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

# ✅ Install Latest Google Chrome
RUN wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome.deb \
    && rm google-chrome.deb

# ✅ Automatically Download Matching ChromeDriver Version
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f1) \
    && CHROMEDRIVER_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json" | jq -r --arg VER "$CHROME_VERSION" '.versions[] | select(.version | startswith($VER)) | .downloads.chromedriver[] | select(.platform == "linux64").url' | head -n 1) \
    && wget -q -O chromedriver.zip "$CHROMEDRIVER_URL" \
    && unzip chromedriver.zip \
    && chmod +x chromedriver \
    && mv chromedriver /usr/local/bin/chromedriver \
    && rm chromedriver.zip

# ✅ Ensure Chrome and Chromedriver Are Installed Correctly
RUN which google-chrome && google-chrome --version
RUN which chromedriver && chromedriver --version

# Start Flask API
COPY . .
CMD exec gunicorn -b 0.0.0.0:5000 app.server:app --workers=1 --threads=2 --timeout 120 --log-level debug
