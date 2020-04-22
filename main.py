import requests
import json
import string
import hashlib

class JulioCesar():

    def __init__(self, token: str):

        self.my_token = token
        self.request = requests.Session()
        self.get_url = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=' + self.my_token
        self.post_url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=' + self.my_token

    def save_json(self):
        
        data = self.request.get(self.get_url).json()
        data = json.dumps(data, indent = 5) 
        with open('answer.json', 'w') as file:
            file.write(data)
        
    def decrypt(self):

        with open('answer.json', 'r') as file:
            data = json.load(file)
        
        shift = data['numero_casas']
        ponctuation = list(string.punctuation)
        alphabet = list(string.ascii_lowercase)
        numbers = list(string.digits)
    
        final_sentence = ""

        for encrypted_word in data['cifrado']:
        
            if(encrypted_word in alphabet):
                index = [index for index, element in enumerate(alphabet) if element == encrypted_word][0]
                decrypt_word = alphabet[index - shift]
                final_sentence = final_sentence + decrypt_word

            elif(encrypted_word in ponctuation or encrypted_word in numbers or encrypted_word == ' '):
                decrypt_word = encrypted_word
                final_sentence = final_sentence + decrypt_word

        data['decifrado'] = final_sentence

        with open('answer.json', 'w') as file:
            data = json.dumps(data, indent = 5) 
            file.write(data)

        return(final_sentence)

    def sha1(self, sentence: str):
        
        sha1_message = hashlib.sha1(sentence.encode('utf-8')).hexdigest()

        with open('answer.json', 'r') as file:
            data = json.load(file)
        
        data['resumo_criptografico'] = sha1_message

        with open('answer.json', 'w') as file:
            data = json.dumps(data, indent = 5) 
            file.write(data)
    
    def submission(self):

        answer = {'answer':open('answer.json', 'rb')}

        response = self.request.post(url = self.post_url, files=answer)
        print(response.status_code)
        print(response.text)
        
if __name__ == '__main__':

    j = JulioCesar(my_token)
    j.save_json()
    sentence = j.decrypt()

    j.sha1(sentence)
    j.submission()