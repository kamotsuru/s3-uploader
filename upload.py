from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from flask_httpauth import HTTPDigestAuth
import boto
import os

'''
アプリコンストラクタ
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

'''
Digest認証
'''
auth = HTTPDigestAuth()

users = {
  "user": os.environ.get('USER_PW')
}

@auth.get_password
def get_password(username):
  if username in users:
    return users.get(username)
  return False

@auth.error_handler
def auth_error():
  response = jsonify({'error': 'unauthorized', 'message': 'Invalid credentials'}
)
  response.status_code = 401
  return response

'''
View設定
'''
@app.route('/upload')
@auth.login_required
def upload():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
      aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
      s3bucket = os.environ.get('S3BUCKET')
      f = request.files['file']
      s3 = boto.connect_s3(aws_access_key, aws_secret_access_key)
      bucket = s3.get_bucket(s3bucket)
      key = bucket.new_key(secure_filename(f.filename))
      key.set_contents_from_file(f) 
      return 'file uploaded successfully'

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)
