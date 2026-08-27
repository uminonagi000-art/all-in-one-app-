from flask import Flask, render_template, request
import os

app = Flask(__name__)

# अपलोड की गई फाइलों को सेव करने के लिए फोल्डर
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'video' not in request.files:
        return "कोई वीडियो अपलोड नहीं हुई है!", 400
    
    video_file = request.files['video']
    category = request.form.get('category')
    language = request.form.get('language')
    dialogue = request.form.get('dialogue')
    
    if video_file.filename == '':
        return "फाइल का नाम खाली है", 400
    
    # वीडियो को सर्वर के 'uploads' फोल्डर में सेव करें
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_path)
    
    return f"""
    <div style="font-family: Arial; text-align: center; margin-top: 50px; background: #0f172a; color: #fff; padding: 40px; border-radius: 10px; max-width: 500px; margin-left: auto; margin-right: auto;">
        <h2 style="color: #38bdf8;">🎉 रिक्वेस्ट सफलतापूर्वक ले ली गई है!</h2>
        <p><b>कैटेगरी:</b> {category}</p>
        <p><b>चुनी गई भाषा/टोन:</b> {language}</p>
        <p><b>आपका डायलॉग:</b> "{dialogue}"</p>
        <p style="color: #fbbf24; margin-top: 20px;">आपकी वीडियो प्रोसेस हो रही है और बहुत जल्द लिप-सिंक के साथ तैयार हो जाएगी!</p>
        <br>
        <a href="/" style="background: #38bdf8; color: #0f172a; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 5px;">वापस जाएं</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
  
