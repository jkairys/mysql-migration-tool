FROM python:3.7
ENV PYTHONPATH="/opt/app:$PYTHONPATH"
COPY src/requirements.txt /opt/app/requirements.txt
RUN pip install -r /opt/app/requirements.txt
COPY src /opt/app
RUN chmod +x /opt/app/migrate.py && chmod +x /opt/app/wait-for-it.sh
WORKDIR "/opt/app"
ENTRYPOINT ["./migrate.py"]
