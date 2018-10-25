# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 5000

# install dependencies
RUN pip3 install -r requirements.txt

# run the application
CMD ["python", "./app.py"]