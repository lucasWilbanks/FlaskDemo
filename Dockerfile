# start by pulling the python image
FROM python:3.6.8 

RUN useradd flaskdemo

# switch working directory
WORKDIR /home/flaskdemo

# copy the requirements file into the image
COPY requirements.txt requirements.txt

# install the dependencies and packages in the requirements file
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip 
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

# copy every content from the local file to the image
COPY app app
COPY migrations migrations
COPY demo.py config.py boot.sh .flaskenv ./
RUN chmod +x boot.sh

ENV FLASK_APP=demo.py
ENV DATABASE_URL=mysql+pymysql://root:password@mysql:3306/flaskdemo

RUN chown -R flaskdemo:flaskdemo ../flaskdemo
USER flaskdemo 

EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT [ "./boot.sh" ]

