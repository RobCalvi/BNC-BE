FROM python:3.11.9-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/app"

# set working directory
WORKDIR /app

# copy requirements
COPY ./requirements.txt /app/requirements.txt
COPY ./app /app/

# install packages without caching
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "*", "--reload"]