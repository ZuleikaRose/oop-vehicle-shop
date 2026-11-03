# "3.15-slim" is a floating tag: it always points at the newest 3.15.x patch
# release. Rebuild with `docker build --pull ...` to pick up those updates.
FROM python:3.15-slim

# Show print()/input() prompts immediately instead of buffering them
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy only the app (see .dockerignore for what is excluded)
COPY car_management.py .

# Don't run as root inside the container
RUN useradd --create-home appuser
USER appuser

CMD ["python", "car_management.py"]
