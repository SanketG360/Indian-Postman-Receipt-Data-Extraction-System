from flask import Flask, render_template, Response, request
import cv2
from PIL import Image, ImageEnhance
import pytesseract
import numpy as np
from threading import Thread


global capture, switch, extract
capture=0
switch=1
extract=0


pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"



#instatiate flask app  
app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)


frame=0
def gen_frames():  # generate frame by frame from camera
    global extract, capture
    while True:
        success, frame = camera.read() 
        if success:   
            if(capture):
                capture=0
                cv2.imwrite("sample.png", frame)
                show(frame)
        
            if(extract):
                extract=0
                cv2.imwrite("postman.jpeg", frame)
                func(frame)

            
                 
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

def func(frame):
    ImagePath = "static/postman.jpeg"
    image_file = Image.open(ImagePath)
   
    cv2.imshow("image_name.jpg",frame
    text = pytesseract.image_to_string(ImagePath)
    pf = text
    res = text.split()
    for i in res:
        if len(i)==13:
            print(i)

    left = 'ts'
    right = 'gms'

    print(pf[pf.index(left)+len(left):pf.index(right)])

    left = 'Amts'
    right = '(Cash)'
    print(pf[pf.index(left)+len(left):pf.index(right)])
    print('successfully')
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show(frame):
    ImagePath = "sample.png"
    image_file = Image.open(ImagePath)
    image_file.save("image_name.jpg", quality=95)
    cv2.imshow("image_name.jpg",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



@app.route('/')
def index():  
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        elif  request.form.get('stop') == 'Stop/Start':
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows() 
            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif request.form.get('Extract')== 'Capture/Extract':
            global extract
            extract=1
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     