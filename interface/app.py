from config import DevConfig
import os
from flask import Flask, flash, request, redirect, url_for ,render_template
from werkzeug.utils import secure_filename   
import pickle
import numpy as np
import mne
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
app.config.from_object(DevConfig)

#pickel model

class model_preperation:
    def __init__(self,file):
        self.file=file
    
    def predict_in_minutes(self,model,features):
            
        epochs=model.predict(features)
        epochs=[round(epoch) for epoch in epochs ]      
        pred_minute=0 if epochs.count(0) > epochs.count(1) else 1
        return pred_minute
            #print(str(A)+" y_pred :",pred_minute,"y_true :",y)
        
    def predict(self):
        features=pd.read_csv(app.config['DATASET_PATH']+self.file)
        features=features.iloc[:,1:]
        features=np.array(features)
        model=pickle.load(open(os.path.join('pkl_objects','voting regressor.pkl'),'rb'))

        label="Concentrate" if self.file[5:7]=='co' else "Non Concentrate"

        prediction= self.predict_in_minutes(model,features)
        
        prediction="Concentrate" if prediction==1 else "Non Concentrate"
        ############################
        return ('Prediction : %s' %\
            (prediction)) , 'Status   : %s'%(label)
        ####################################




ALLOWED_EXTENSIONS = {'csv'}
## allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

x=100
#####################
@app.route('/', methods=['GET', 'POST'])
def home():
    img_path_con='static/assets/img/img_path/con1.png'
    img_path_noncon='static/assets/img/img_path/ncon1.png'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print("###########################################")
        print("file path name : ",secure_filename(file.filename))
        print("path           : ",app.config['DATASET_PATH'])
        print("###########################################")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            model=model_preperation(filename)
            predict,status=model.predict()

            ### plot part ########################################
            path='dataset/edf_dataset/'
            filename_number=filename[9] if filename[10] =='.' else filename[9:11]
            filename_number=f"{int(filename_number):02}"
            filename_path=path+"S0"+filename_number+"E02.edf"
            import mne
            datax=mne.io.read_raw_edf(filename_path,preload=True) 
            ### choose min for prediction 
            choose = filename[5:7]
            if choose=="co":
                image=datax.compute_psd(tmin=60,tmax=120,fmin=13,fmax=39, picks=[2],method='multitaper').plot()
            else :
                image=datax.compute_psd(tmin=120,tmax=180,fmin=13,fmax=39, picks=[2],method='multitaper').plot()

            image.savefig('static/images/new_plot.png')
            ######################################################
            return render_template('index.html', 
            img_path_con=img_path_con,
            img_path_noncon=img_path_noncon,
            predict=predict,
            status=status,
            pred_plot='static/images/new_plot.png')
    
    
    return render_template('index.html',
    img_path_con=img_path_con,
    img_path_noncon=img_path_noncon)


from flask import Response
import io

@app.route('/plot.png')
def plot_png():
    output = io.BytesIO()
    plot_image=FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
