#Folder Structure(for now)
- Model_data/ #Raw data collected from ADXL345 on 16th Jan
  #Sensor Configuration and Data Collection
- ADXL345.py #Sensor communication protocol
- Database.py #Creates connection between postgreSQL server and RPI
- main.py 

  #Analysis
-  Signal Processing.ipynb #Time-, Frequency-Domain feature analysis including envelope spectrum
-  Spectrogram_ML #CNN model trained on T-F spectrogram of'Model_data'

#Instruction
1. Clone the respository
2. Create Virtual Environment and Install dependencies: `pip install -r Requirements.txt`
3. Open Jupyter Notebook: `jupyter notebook`
4. 
