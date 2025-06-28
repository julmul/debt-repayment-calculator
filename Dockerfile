FROM python

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install bokeh numpy

EXPOSE 5006

COPY . /app/
WORKDIR /app


# Command to run the Bokeh app
CMD ["bokeh", "serve", "main.py", "--allow-websocket-origin=*", "--port=5006", "--address=0.0.0.0"]