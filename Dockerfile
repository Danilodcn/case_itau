FROM ubuntu

COPY . /app
WORKDIR /app

# # RUN pip install -U pip 
RUN apt update && apt upgrade -y

RUN apt install python3 -y && \
    apt install python3-pip -y

RUN apt install python3.8-venv -y && \
    python3 -m venv /.venv && \
    /bin/bash -c "source /.venv/bin/activate"
# RUN apt --no-cache add \
#     python python-pip
# RUN pip install pipenv

# RUN echo "OLa" && \
#     pipenv shell && \
#     pipenv install

RUN pip install -r requirements.txt

# CMD python3 /app/app.py

ENTRYPOINT [ "python3", "/app/app/app.py" ]