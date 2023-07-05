from flask import Flask, render_template, request
import requests
import os
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
  if request.method == 'POST':
    user_input = request.form['user_input']
    record_type = request.form['record_type']
    record_name = request.form['record_name']
    record_content = request.form['record_content']
    zone_id = request.form['zone_id']
    return cloudflare(user_input,record_type,record_name, record_content, zone_id)
  return render_template('index.html')

def cloudflare(user_input,record_type, record_name, record_content, zone_id):
  cloudflare_api = user_input
  cloudflare_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
  headers = {
    "Authorization": f"Bearer {cloudflare_api}",
    "Content-Type": "application/json"
  }
  payload = {
    "type": record_type,
    "name": record_name,
    "content": record_content
  }
  response = requests.post(cloudflare_url,headers=headers,data=json.dumps(payload))
  if(response.status_code == 200):
    return render_template('mainpage.html')
  else:
    error_code = response.text
    return render_template('error.html',error_code=error_code)
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080)
