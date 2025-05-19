FROM node:20-slim

WORKDIR /usr/src

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget unzip default-jre curl jq git \
    && rm -rf /var/lib/apt/lists/*

# Install SonarScanner
ENV SONAR_SCANNER_VERSION=4.8.0.2856
ENV SONAR_SCANNER_HOME=/opt/sonar-scanner
RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}.zip && \
    unzip sonar-scanner-cli-${SONAR_SCANNER_VERSION}.zip && \
    mv sonar-scanner-${SONAR_SCANNER_VERSION} ${SONAR_SCANNER_HOME} && \
    rm sonar-scanner-cli-${SONAR_SCANNER_VERSION}.zip

ENV PATH="${SONAR_SCANNER_HOME}/bin:${PATH}"

COPY sonar-project.properties ./sonar-project.properties

CMD ["sonar-scanner"]
