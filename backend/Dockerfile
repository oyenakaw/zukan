FROM python:3-onbuild

ENV PORT 3001
COPY . /usr/local/app
RUN pip install --upgrade pip
#RUN pex --disable-cache -r requirements.txt -v -c gunicorn -o predict.pex
#ENTRYPOINT bash export.sh
CMD exec gunicorn app:app --bind :$PORT --workers 1 --threads 8 --worker-class gevent --timeout 180 --log-level DEBUG