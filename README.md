# ClipWiz
This is the official repository of 2022 Shanghai Undergraduate Training Program for Innovation and Entrepreneurship _Assistant for Automatic Generation of Video Highlights in Multiple Scenarios._

![image.png](https://cdn.nlark.com/yuque/0/2024/png/39055961/1708138852223-d4b94d35-7736-404d-b5c7-e3764cf30a7d.png#averageHue=%236a6969&clientId=uc27b20fe-9fce-4&from=paste&height=470&id=u71acb1c9&originHeight=811&originWidth=864&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=55469&status=done&style=none&taskId=u9e60dfe5-1277-48a6-9d79-3971f588251&title=&width=500.20001220703125)
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

1. You can run our web application like the script in the below:
```
python app.py
```
Notice, running our web application on GPUs can speed up processing.

2. The main interface of our web application is shown below:

![网站首页.jpg](https://cdn.nlark.com/yuque/0/2024/jpeg/39055961/1708138655832-d7e7365b-1ea8-4ac6-9981-d06c3faf2963.jpeg#averageHue=%231a2030&clientId=uc27b20fe-9fce-4&from=ui&id=u964c9b82&originHeight=938&originWidth=1906&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=371747&status=done&style=none&taskId=uf1913b0f-019a-4f15-bc4c-bf699d6e079&title=)

- If you want to use the "Bilibili" function module on the left side, you first need to upload the URL or BV number of the video whose highlights you want to watch. After successful reception and completion of back-end processing, the video will be opened directly from bilibili waiting for you to play. With the help of Selenium, it is possible to simulate the operation of adjusting video progress, achieving the effect of only playing highlight clips.
- If you want to use the "Football" function module on the right side, you first need to upload a soccer match video from local. After successful reception and completion of back-end processing, online viewing and download options will be available for you to choose from.
## Project members
| Leader | Kaiheng Qian |  |  |  |
| --- | --- | --- | --- | --- |
| Members | Xiang Liao | Chenlei Zhu | Donghao Li | Yifei Long |

