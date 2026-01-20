# Folder Structure(for now)
- Model_data/ :Raw data collected from ADXL345 on 16th Jan
  ### Sensor Configuration and Data Collection
- ADXL345.py :Sensor communication protocol
- Database.py :Creates connection between postgreSQL server and RPI
- main.py 

  ### Analysis
-  Signal Processing.ipynb :Time-, Frequency-Domain feature analysis including envelope spectrum
-  Spectrogram_ML :CNN model trained on T-F spectrogram of'Model_data'

# Model Training
1. The first cell in **Signal Processing.ipynb** generates the vibration spectrogram
   - Change `condition` and `speed` variables to select corresponding dataset
   - Run the cell and it will create `Spectrogram` folder that stores spectrogram imges
2. The next cell retreives training data from `Spectrogram` folder including two classes(old and new)
3. Change layer structure in `train_model` function
