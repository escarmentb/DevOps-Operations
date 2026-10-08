FROM nginx:alpine

COPY site/ /usr/share/nginx/html/

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD wget --quiet --output-document=/dev/null \
  http://localhost/health || exit 1
