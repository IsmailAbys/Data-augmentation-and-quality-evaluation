# Data-augmentation-and-quality-evaluation
Data augmentation and quality evaluation of generated data

# Installation
Before executing the code, you must first install the libraries in the requirements file and make sure you have the correct versions installed.

`pip install -r requirements.txt`


# Python scripts and their function
The folder `Data_Aug_&_Quality_evaluation` contains all files.
`data_aug.py` contains all functions (brightness, flipping, elastic deformation, 30° and 90° rotation) and run it with \
```Python 
if __name__ == "__main__": 
        Data_aug.functionName(original_data)
```



---
# Quantitative analysis
`MSE.py`, `ssim.py` and `Distance_euclidean.py` are the metrics for evaluating the quality of the images generated. Run
`Python file.py`.

---
# Qualitative analysis
To qualitatively analyze the synthetic data, run the file `visualization.py`. press "b" for the broghtness, "r" for the 30° rotation and "o" for the original data.
