FROM python:2.7-alpine3.6
RUN pip install RainEagle || echo ignore
COPY power.py /
EXPOSE 8080
CMD python /power.py