# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

################################
# BUILDER-BASE
################################

# 1. force platform to the current architecture to increase build speed time on multi-platform builds
FROM --platform=$BUILDPLATFORM node:lts-bookworm-slim AS builder-base
COPY src/frontend /frontend

# PUPPETEER_SKIP_DOWNLOAD: puppeteer (via accessibility-checker, test-only)
# must not download Chrome here - the build env can't fetch it and the
# production image never runs it.
RUN cd /frontend && PUPPETEER_SKIP_DOWNLOAD=true npm install && npm run build

################################
# RUNTIME
################################
FROM nginxinc/nginx-unprivileged:stable-bookworm-perl AS runtime

LABEL org.opencontainers.image.title=langflow-frontend
LABEL org.opencontainers.image.authors=['Langflow']
LABEL org.opencontainers.image.licenses=MIT
LABEL org.opencontainers.image.url=https://github.com/langflow-ai/langflow
LABEL org.opencontainers.image.source=https://github.com/langflow-ai/langflow

USER root

RUN groupadd --gid 10000 langflow \
    && useradd --uid 10000 --gid langflow --create-home --shell /usr/sbin/nologin langflow

COPY --from=builder-base --chown=langflow:langflow /frontend/build /usr/share/nginx/html
COPY --chown=langflow:langflow ./docker/frontend/start-nginx.sh /start-nginx.sh
COPY --chown=langflow:langflow ./docker/frontend/default.conf.template /etc/nginx/conf.d/default.conf.template

RUN chmod +x /start-nginx.sh

USER 10000:10000

ENTRYPOINT ["/start-nginx.sh"]
