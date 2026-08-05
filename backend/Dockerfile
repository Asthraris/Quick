FROM python:3.12-slim  

# 2. Set environment variables to optimize Python inside Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /backend
# When you pass variables using -e (or --env), Docker injects those key-value pairs directly into the container's operating system environment
COPY . .
RUN pip install -r requirements/prod.txt

EXPOSE 8000

CMD ["fastapi","run" , "main.py"]