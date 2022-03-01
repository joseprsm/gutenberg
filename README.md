# Gutenberg :feather:

Gutenberg is a tool that uses GPT-3 to generate marketing short copy, 
such as LinkedIn, Google Search and Facebook ads. The model is used to generate text that is 
relevant to the target audience and the product or service being marketed.

## Quickstart

To get everything running, just run the following commands, setting the `OPENAI_API_KEY`
environment variable to your own. 

```shell
$ export OPENAI_API_KEY=<your_API_key>
$ docker-compose up -d
```

That should spin up three containers:

* `db` with a postgres image
* `backend` with FastAPI application, serving as the middleman between the streamlit application and the GPT-3 endpoint
* `frontend` with the Streamlit application