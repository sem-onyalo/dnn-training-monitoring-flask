# GAN Training Monitor Web Application

A Flask web application to monitor GAN training runs.

## Install

### Windows

```
python -m venv env

.\env\Scripts\activate

pip install -r requirements.txt
```

## Run

```
python app.py
```

### Run with AWS S3 Backend

```
python app.py --storage aws_s3
```
