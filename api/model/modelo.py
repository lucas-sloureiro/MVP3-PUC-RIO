import numpy as np
import pickle
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
class Model:
    
    def carrega_modelo(path):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra
        """
        
        if path.endswith('.joblib'):
            model = joblib.load(path)
        elif path.endswith('.pkl'):
            with open(path, 'rb') as file:
                model = pickle.load(file)

        else:
            raise Exception('Formato de arquivo não suportado')
        return model
    
    def preditor(model, form):
        """Realiza a predição de pinguins com base no modelo treinado
        """
        X_input = np.array([form.lenght, 
                            form.depth, 
                            form.flipper, 
                            form.mass
                        ])

        # Aplica scaler nos dados assim como foi treinado no modelo
        diagnosis = model.predict(X_input.reshape(1, -1))
        return str(diagnosis[0])