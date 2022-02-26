import os
import openai

from flask import Flask, request

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["POST"])
def index():
    name = request.json.get('item_name')
    description = request.json.get('item_description')
    target_audience = request.json.get('target_audience', 'businesses')
    platform = request.json.get('platform', 'LinkedIn')
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=generate_prompt(name, description, platform, target_audience),
        temperature=0.6, n=1, max_tokens=1000)
    return {'result': [
        x.text for x in response.choices
    ]}


def generate_prompt(product_name=None, product_description=None, platform='LinkedIn', target_audience=None):
    return f"""
        Write an ad for the following product to run on {platform} aimed at {target_audience}:
        
        Product: {product_name}. {product_description}.
        """


if __name__ == '__main__':
    app.run()
