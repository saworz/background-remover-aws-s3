project_name
==============================

A short description of the project.

Project Organization
------------

	├── README.md          <- The top-level README for developers using this project.
	│
	├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
	│                         generated with `pip freeze > requirements.txt`
	│
	├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
	│
	├── Animals_classification_VGG16                <- Source code for use in this project.
	│   ├── __init__.py    <- Makes src a Python module
	│   │
	│   ├── data           <- Scripts to handle data
	│   │   └── extract_dataset.py <- Unzips dataset
	│   │   └── get_images.py      <- Gets list of all .jpeg, .jpg or .png files in dir
	│   │   └── parse_data.py      <- Data parser
	│   │   └── split_folders.py   <- Splits data into training and validation dirs
	│   │
	│   │
	│   ├── features       <- Scripts to turn raw data into features for modeling
	│   │   └── handle_input.py    <- Used to choose between training and loading model
	│   │   └── image_folder.py    <- Custom ImageFolder class for data validation
	│   │   └── predict_custom_image.py  <- Used to validate model on a custom data
	│   │
	│   │
	│   ├── model        <- Scripts to train/load/save model
	│   │   │── create_model.py    <- Initialize new model                
	│   │   ├── load_model.py      <- Load existing weights to the model
	│   │   └── save_model.py      <- Save trained model's weights to file
	│   │   └── training.py        <- Training pipeline
	│   │
	└── tox.ini            <- tox file with settings for running tox


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
