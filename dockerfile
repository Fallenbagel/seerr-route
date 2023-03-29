FROM python:3

ENV seerr_baseurl ''
ENV seerr_api_key ''
ENV movieFolder_Animemovies ''
ENV movieFolder_Cartoon '' 
ENV tvFolder_documentary ''
ENV tvFolder_Animatedseries ''
ENV tvFolder_documentary ''
ENV tvFolder_reality ''

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD main.py /

CMD [ "python", "./main.py" ] 
