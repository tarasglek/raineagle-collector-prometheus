# docker build . -t power-exporter
# docker tag power-exporter tarasglek/power-exporter
# docker push tarasglek/power-exporter
FROM python:2.7-alpine3.6
RUN pip install RainEagle || echo ignore
COPY power.py /
EXPOSE 8080
CMD python /power.py