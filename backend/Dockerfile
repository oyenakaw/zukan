FROM python:3.7
RUN pip install --upgrade pip
ENV PORT 3001
WORKDIR /usr/local/app
COPY . /usr/local/app
RUN pip install -r requirements.txt

#RUN pex --disable-cache -r requirements.txt -v -c gunicorn -o predict.pex
#ENTRYPOINT bash export.sh
CMD exec gunicorn app:app --bind :$PORT --workers 1 --threads 8 --worker-class gevent --timeout 180 --log-level DEBUG