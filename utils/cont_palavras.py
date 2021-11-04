import pandas as pd
import glob
import os

json_paths = glob.glob("./guias_com_json/*.json")

lista = []
for path in json_paths:
    
    try:    
        text = open(path, 'r').read()
        dic_text = eval(text)
        
        for n,page in enumerate(dic_text["guias"]):
            page = page[f"page_{n+1}"]
            lista.append([os.path.basename(path),n+1,
                        page["palavras_manuscritas"],page["palavras_digitadas"],
                        page["palavras_manuscritas"]/(page["palavras_manuscritas"]+page["palavras_digitadas"])])
    except:
        print(path)
        os.remove(path)

df = pd.DataFrame(data=lista,columns=["documento","page","palavras_manuscritas","palavras_digitadas","pc_palavras_manuscritas"])
df.to_csv("./n_palavras.csv",index=False)
print(df)