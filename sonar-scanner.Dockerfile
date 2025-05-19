FROM node:20-slim

WORKDIR /usr/src

# Install dependencies required for SonarScanner
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    default-jre \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install SonarScanner
ENV SONAR_SCANNER_VERSION=4.8.0.2856
ENV SONAR_SCANNER_HOME=/opt/sonar-scanner
RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}.zip && \
    unzip sonar-scanner-cli-${SONAR_SCANNER_VERSION}.zip && \
    mv sonar-scanner-${SONAR_SCANNER_VERSION} ${SONAR_SCANNER_HOME} && \
    rm sonar-scanner-cli-${SONAR_SCANNER_VERSION}.zip

# Add sonar-scanner to the PATH
ENV PATH="${SONAR_SCANNER_HOME}/bin:${PATH}"

# Add wait script (if needed)
COPY scripts/sonar/wait-for-sonarqube.sh /wait-for-sonarqube.sh
RUN chmod +x /wait-for-sonarqube.sh

WORKDIR /usr/src

CMD ["sonar-scanner"]
