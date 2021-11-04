import glob



def chaves_valores(path): # mostra tudo entro de dados
    text = open(path, 'r').read()
    dic_text = eval(text)

    print("mostrando valores e chaves")
    guias = dic_text['guias']
    for s in guias:
        for pagen in s:
            for key in s[pagen]['dados']:
                print(f"key: {key} \n value:{s[pagen]['dados'][key]}")
                print("#############################################")

def chaves_especifica(path,key='cliente'): # mostra chave especifica dentro de dados
    text = open(path, 'r').read()
    dic_text = eval(text)

    print("mostrando valores e chaves")
    guias = dic_text['guias']
    for s in guias:
        for pagen in s:
            print(f"key: {key}: \nvalue:{s[pagen]['dados'][key]}")
            print("#############################################")


for path in glob.glob("./*json"):
    print(path)
    chaves_especifica(path)

    print("##################################################################################")