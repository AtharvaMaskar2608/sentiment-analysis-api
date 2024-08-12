# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

WORKDIR /code

# RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade pip
RUN chmod 1777 /tmp
RUN apt-get update && apt-get install -y \
python3-pip

EXPOSE 9099

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV APP_PORT=9099

# Install pip requirements
COPY requirements.txt /code/requirements.txt
# RUN pip3 install torchvision==0.10.1
RUN pip3 install --no-cache-dir -r /code/requirements.txt
#RUN pip3 install torch==1.10.2
COPY . /code
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

CMD ["uvicorn", "fastapi_app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "9099"]


