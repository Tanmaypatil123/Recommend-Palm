import os
import dotenv
import google.generativeai as palm
import re
import requests
from constants import SESSION_HEADERS
# from utils import urlify_string
import time
import urllib.parse
import streamlit as st

dotenv.load_dotenv()

class Recommend_movies:
    def __init__(self) -> None:
        self.model = palm
        self.model.configure(api_key=os.getenv("PALM_API_KEY"))

        self.session = requests.Session()
        self.session.headers = SESSION_HEADERS

        self.defaults = {
            'model': 'models/text-bison-001',
            'temperature': 0.7,
            'candidate_count': 1,
            'top_k': 40,
            'top_p': 0.95,
            'max_output_tokens': 1024,
            'stop_sequences': [],
            'safety_settings': [
                {"category":"HARM_CATEGORY_DEROGATORY","threshold":1},
                {"category":"HARM_CATEGORY_TOXICITY","threshold":1},
                {"category":"HARM_CATEGORY_VIOLENCE","threshold":2},
                {"category":"HARM_CATEGORY_SEXUAL","threshold":2},
                {"category":"HARM_CATEGORY_MEDICAL","threshold":2},
                {"category":"HARM_CATEGORY_DANGEROUS","threshold":2}
            ],
        }
    
    def urlify_string(self,string):
        url_encoded = urllib.parse.quote(string)
        return url_encoded
    
    def generate(self,movie_name = str):

        result = []
        
        prompt = f"""input: Th Dark Knight 
            output: Batman Begins
            The Prestige
            Se7en
            Fight Club
            The Shawshank Redemption
            input: {movie_name}
            output:"""

        response = self.model.generate_text(
            **self.defaults,
            prompt=prompt
        )
        
        recommendations = response.result.split("\n")
        time.sleep(0.1)
        for i in recommendations:
            movie = self.urlify_string(i)
            url = f"https://api.themoviedb.org/3/search/movie?query={movie}&include_adult=false&language=en-US&page=1"
            res = self.session.get(url).json()
            result.append(res["results"])
            

        return result



st.title("Recommendation System Using Palm")
text_box = st.text_input("Your movie goes here 🎥")
col1, col2 = st.columns(2)

r_m = Recommend_movies()

if text_box :

    print(text_box)

    result = r_m.generate(str(text_box))
   
    for i in range(len(result)) :
        if result[i] != []:
            
            if i % 2 == 0 : 

                col1.image(f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{result[i][0]['poster_path']}")
                col1.write(result[i][0]['title'])
            else :
                
                col2.image(f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{result[i][0]['poster_path']}")
                col2.write(result[i][0]['title'])
        
