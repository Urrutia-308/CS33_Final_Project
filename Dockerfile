FROM python:3.9-slim

#set the working directory in the container to /app
WORKDIR /app

#copy the current directory contents into the container at /app
COPY . /app

#install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#make port 5000 available to the world outside this container
EXPOSE 5000

#define environment variable
ENV NAME World

#run app.py when the container launches
CMD ["python", "./backend/app.py"]
