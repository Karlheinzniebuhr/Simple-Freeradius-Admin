# base image
FROM python:3-onbuild

## The maintainer name and email
MAINTAINER Karl Niebuhr <karlbooklover@gmail.com>

EXPOSE 5000

# install dependencies
RUN pip3 install -r requirements.txt

# run the application
CMD ["timeout", "1m"]
# CMD ["python", "./SimpleAdmin/init_default_admin.py"]
CMD ["python", "./app.py"]