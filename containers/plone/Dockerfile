# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.1
FROM plone/plone-backend:${PLONE_VERSION}

RUN <<EOT
  /app/bin/pip install collective.person
EOT

ENV SITE=Plone
ENV SITE_ID=Plone
ENV DELETE_EXISTING=1
ENV DISTRIBUTION=volto
ENV ADDITIONAL_PROFILES=collective.person:default
