from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
import os

img_folder = os.path.join('static','images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = img_folder

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/date_recived' , methods = ["GET","POST"])
def date_recived():
    if request.method == 'POST':
        year1 = request.form.get("1year")
        month1 = request.form.get("1month")
        day1 = request.form.get("1day")
        year2 = request.form.get("2year")
        month2 = request.form.get("2month")
        day2 = request.form.get("2day")

        mdate = year1+'/'+month1+'/'+day1
        fdate = year2+'/'+month2+'/'+day2

        malepage = requests.get("https://lunaf.com/lunar-calendar/"+mdate)
        femalepage = requests.get("https://lunaf.com/lunar-calendar/"+fdate)   
        
        malesouped = BeautifulSoup(malepage.content,"html.parser")
        femalesouped = BeautifulSoup(femalepage.content,"html.parser")

        maleimgs = malesouped.find_all("img")
        femaleimgs = femalesouped.find_all("img")

        
        maleimgli = maleimgs[0].attrs.get("src")
        femaleimgli = femaleimgs[0].attrs.get("src")

        maleimglink = "https://lunaf.com"+maleimgli
        femaleimglink = "https://lunaf.com"+femaleimgli

        maleimage = requests.get(maleimglink).content
        femaleimage = requests.get(femaleimglink).content

        malefilename = r"static/images/" + "male.png"
        femalefilename = r"static/images/" + "female.png"  

        with open(malefilename,"wb") as malefile:
            malefile.write(maleimage)

        with open(femalefilename,"wb") as femalefile:
            femalefile.write(femaleimage)

        male_img = os.path.join(app.config['UPLOAD_FOLDER'],'male.png')
        female_img = os.path.join(app.config['UPLOAD_FOLDER'],'female.png')

    
        return render_template('moon.html',male_img=male_img,female_img=female_img)


if __name__ == '__main__':
    app.run(debug=True)