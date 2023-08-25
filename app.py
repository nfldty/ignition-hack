from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import cv2
import secrets
import os

#image = Image.open('image.png', mode='r')
#print(image_to_string(image))
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    
    if request.method == 'POST':
        file = request.files.get('file')
        
        filename, extension = file.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".{extension}"
        

        raw_file_location = os.path.join(os.getcwd(), "static", "saved_img" , generated_filename)
        file.save(raw_file_location)

        # print(file_location)

        # OCR here
        pytesseract.pytesseract.tesseract_cmd = rf'{os.getcwd()}\\Tesseract-OCR\\tesseract.exe'
       
        #img = Image.open(file_location)
        img = cv2.imread(raw_file_location)
    
          
        raw = pytesseract.image_to_string(img)
        converted_text = raw.split()
        
        d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        print(d.keys())
        for i in range(len(d["conf"])):
            print([d[key][i] for key in d])
        data_size = len(d["text"])
        cur_level = [(0, 0, 0, 0, 0), (0, 0, 0)]
        text_size = 0
        for i in range(data_size):
            if int(d['conf'][i] >= 60):
                text_size += d['height'][i]
                if (d['level'][i] ,d['page_num'][i], d['block_num'][i], d['par_num'][i], d['line_num'][i]) == cur_level[0]:
                    
                    d['top'][i], d['height'][i] = cur_level[1]
                else:
                    cur_level[0] = (d['level'][i] ,d['page_num'][i], d['block_num'][i], d['par_num'][i], d['line_num'][i])
                    cur_level[1] = (d['top'][i], d['height'][i])

            i += 1
        
        text_size /= data_size
        for i in range(len(d["conf"])):
            print([d[key][i] for key in d])  
        
        '''
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        
        saved_img = Image.fromarray(img, "RGB")
        saved_img.save('testingtestingtesting.png')
        #saved_img.show()
        
        cv2.imshow('img', img)
        cv2.waitKey(0)
        '''
        
        return render_template('upload.html', d=d, font_size=text_size, data_size=data_size, converted_text=converted_text, img_url=raw_file_location, filename=generated_filename)
    
    else:
        
        return render_template('upload.html')           

'''
@app.route('/converted', methods=['POST', 'GET' ])                
def converted():
    return render_template('upload.html', converted_text=converted_text)
'''