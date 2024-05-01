FROM python:3.12
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install -r requirements.txt
# run app
CMD ["python", "randomMovieRouletteBot.py"]

