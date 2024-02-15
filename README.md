# ClipWiz
This is the official repository of 2022 Shanghai Undergraduate Training Program for Innovation and Entrepreneurship _Assistant for Automatic Generation of Video Highlights in Multiple Scenarios._
## Repository structure
```
flaskProject/
│  app.py                                    // script program
│  requirements.txt                          // environment dependencies
│  
├─danmu                                      // code related to bilibili highlights
│  │  danmu_analysis.py                      // main calling program
│  │  danmu_counts_helper_functions.py       // danmu count analysis
│  │  danmu_emotion_helper_functions.py      // danmu emotion analysis
│  │  danmu_evaluation_functions.py          
│  │  danmu_highlights_play.py               // play highlights
│  │  danmu_other_helper_functions.py        
│  │  emotion.py
│  │  
│  └─dict                                    // store dictionaries
│      AdverbOfDegree.txt                    // dictionary of adverbs of degree
│      BosonNLP.txt                          // dictionary of BosonNLP
│      NegativeWords.txt                     // dictionary of negative words
│      StopWords.txt                         // dictionary of stop words
│          
├─soccer                                     // code related to soccer highlights
│  │  soccer_analysis.py                     // main calling program
│  │  soccer_audio_helper_functions.py       // audio analysis
│  │  soccer_cv_helper_functions.py          // visual analysis
│  │  soccer_evaluation_functions.py         
│  │  soccer_other_helper_functions.py       
│  │  
│  └─mobilenetv3                             // scene recognition model
│      class_indices.json                    // train data
│      mobilenet_v3.pth                      // store raw model
│      model_v3.py                           // model building
│      predict.py                            // model prediction
│      train.py                              // model training
│      trained_model.pth                     // store trained model
│          
├─static                                     // store static files
│  ├─css
│  │   bilibili.css
│  │   football.css
│  │   index.css
│  │   loading.css
│  │      
│  ├─images
│  │   clipwiz.png
│  │   star.jpg
│  │      
│  └─js
│      football.js
│      index.js
│      loading.js
│          
└─templates                                  // store HTML templates
    bilibili.html
    football.html
    index.html
    loading.html
```
## Setup

1. Enter the flaskProject directory.
```
cd flaskProject
```

2. To install the environment dependencies needed to run the code, you can simply run
```
pip install -r requirements.txt
```

3. Other necessary installations and configurations.
- To run our web application, make sure you have the [Microsoft Edge browser](https://www.microsoft.com/zh-cn/edge/download?form=MA13FJ)
- Download the [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads) that corresponds to your browser version and place it in the right directory
- Install the [Selenium IDE](https://microsoftedge.microsoft.com/addons/detail/selenium-ide/ajdpfmkffanmkhejnopjppegokpogffp) from the homepage of Microsoft Edge Extensions and keep it on
## Run pipeline
You can run our web application like the script in the below:
```
python app.py
```
Notice, running our web application on GPUs can speed up processing.
## Project members
| Leader | Kaiheng Qian |  |  |  |
| --- | --- | --- | --- | --- |
| Members | Xiang Liao | Chenlei Zhu | Donghao Li | Yifei Long |

