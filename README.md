# EUROMILLION APP v1.0.0
## ABOUT US
Sylvain JALBERT IA <jalbertsyl@cy-tech.fr>  
Romain ROYER ICC <royerromai@cy-tech.fr>    

## IMPORT

python v3.10+ 
fastapi v0.650.0+ 
uvicorn v0.16.0+ 
## QUICK START

-Stay in root folder ```./euro-millions```
-Run bash ``` ./build.sh``` to unzip needed files
-Run ```uvicorn main:app --reload```
-Go to http://127.0.0.1:8000/docs#/
Enjoy the API :)
## KNOWN BUG

If the Generation of a Winning ticket return 0. You should delete ```euro-millions\api\endpoints\model\random_forest.joblib```
and unzip again the .joblib file from ```random_forest.tar.xz```. It seems that training again or adding data modify badly the model, making the API Request returning 0.

# MORE INFORMATIONS

```euro-millions\datasource\analyse_datas.ipynb``` -> allows you to understand our data and analyze.

```euro-millions\api\endpoints\dev\create-ml-model.ipynb``` -> allows you to create a dataset (win and lose tickets) with the number of loosing tickets for each winning one that you want.
