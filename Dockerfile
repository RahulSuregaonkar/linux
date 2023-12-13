FROM python:3.8

# Install Git
RUN apt-get update && \
    apt-get install -y git


LABEL maintainer="rahuldemostore.co.in"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Clone the Git repository
RUN git clone https://github.com/RahulSuregaonkar/Final_main_Django.git .

# Install dependencies (if any)
# RUN pip install -r requirements.txt

# Activate the virtual environment
RUN /bin/bash -c "source venv/Scripts/activate"

# Continue with your Dockerfile setup, such as running Django migrations or starting the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]