FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV google_api_key = 'AIzaSyCrBweCSMeZybW-TM18-wHay85ZiwfYvew'
ENV rapidapi_key = '4bc37fb47cmsh69359cf16c12ce8p1dcc10jsn88bef5d578d3'
ENV search_engine_cx = '22fed8160f8634eca'
ENV mysql_password = '07170'
EXPOSE 8080
CMD ["gunicorn", "-b", ":8080", "app:app"]
