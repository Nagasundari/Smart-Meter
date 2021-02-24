FROM python
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt 
ENTRYPOINT ["bash"] 
CMD ["run.sh"]