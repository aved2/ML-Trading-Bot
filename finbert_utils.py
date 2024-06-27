from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 

#Check if gpu available
device = "cuda:0" if torch.cuda.is_available() else "cpu"

#Hugging Face tokenization based on finbert vocabulary model, 
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

#Load hugging face model for sentiment analysis, calcs sentiment based on finbert model with gpu/cpu
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)

labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news):
    if news:
        #Convert text into tokens, return as pytorch tensors
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        #Return raw logits from model
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        
        #Convert logits into probabilities with softmax
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)

        #Extract probability and sentiment
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]

        return probability, sentiment
    else:
        return 0, labels[-1]


if __name__ == "__main__":
    tensor, sentiment = estimate_sentiment(['markets responded negatively to the news!','traders were displeased!'])
    print(tensor, sentiment)
    print(torch.cuda.is_available())