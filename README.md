
# qaptnet
**qaptnet** is an implementation of the [BERT](https://github.com/google-research/bert) model,
fined tuned for question-answering tasks, trained on a Portuguese dataset. 
Its objective is, given a question and a context, i.e. a snippet of
text that contains the answer to the given question, output the start and end token index that
spans the answer.
This repository contains a dockerized API built over qaptnet for integrate it into the ELG. 

# Installation and running:
 For running the original project:
 - Get the code of the original repository https://github.com/nunorc/qaptnet . Change the library pytorch transformers 
   by transformers and add the parameter `return_dict=False` in self.model() instruction in `qaptnet.py`. Finally 
   follow the instructions of the original Readme.
 
For running the Microservs project:
1) Build the image:
```
sh docker-build.sh
```
2) Run the container:
```
docker run --rm -p 8866:8866 elg_qapnet:1.0
```
3) Make requests to the API:
- Create a JSON file with the fields `context` and `question`, then:
```
curl -H "Content-Type: application/json" --data @test_file.json http://0.0.0.0:8866/predict_json
```

```
curl -X POST  http://0.0.0.0:8866/predict_json -H 'Content-Type: application/json' -d '{"type":"text", "content":"Arquitetonicamente, a escola tem um caráter católico. No topo da cúpula de ouro do edifício principal é uma estátua de ouro da Virgem Maria.", "params":{"question":"De quem é a estatua de ouro?"}}'
```


# Test
In the folder `test` you have the files for testing the API according to the ELG specifications.
It uses an API that acts as a proxy with your dockerized API that checks both the requests and the responses.
For this follow the instructions:
1) Check out the .env file which has the data of the image and of your API. You should not change anything here.
2) Launch the test: `docker-compose up`
3) Make the requests, instead of to your API's endpoint, to the test's endpoint:
```
curl -X POST  http://0.0.0.0:8866/processText/service -H 'Content-Type: application/json' -d '{"type":"text", "content":"Arquitetonicamente, a escola tem um caráter católico. No topo da cúpula de ouro do edifício principal é uma estátua de ouro da Virgem Maria.", "params":{"question":"De quem é a estatua de ouro?"}}'
```
4) If your request and the API's response is compliance with the ELG API, you will receive the response.
   1) If the request is incorrect: Probably you will don't have a response and the test tool will not show any message in logs.
   2) If the response is incorrect: You will see in the logs that the request is proxied to your API, that it answers, but the test tool does not accept that response. You must analyze the logs.


# Original repository
 - [Link of original repository](https://github.com/nunorc/qaptnet) 
 - Original project has a MIT License

# Original repository README

**qaptnet** is an implementation of the [BERT](https://github.com/google-research/bert) model,
fined tuned for question-answering tasks, trained on a Portuguese dataset. The model is
available from the `model-pretrained` directory, as a [PyTorch](https://pytorch.org/) model,
and the training process was performed using the
[pytorch-transformers](https://github.com/huggingface/pytorch-transformers) package.
In an nutshell the goal of the model is: given a question, and a context, i.e. a snippet of
text that contains the answer to the given question, output the start and end token index that
spans the answer.

The question-answering dataset is available from the
[squad-v1.1-pt](https://github.com/nunorc/squad-v1.1-pt) repository, a Portuguese
translation of the [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) dataset.

`qaptnet.py` is a simple Python package to interface with the pre-trained
model. Check the `requirements.txt` file for the package dependencies.

## Synopsis

```
python
# import the model
from qaptnet import qaptnet

# create a new default object
ptnet = qaptnet()

# query the model
ptnet.query(context = context, question = question)
```

## Examples

The following snippets illustrate some examples of queries to the model, for the question
and corresponding context.

```
python
context = """Arquitetonicamente, a escola tem um caráter católico. No topo da cúpula de ouro
do edifício principal é uma estátua de ouro da Virgem Maria. Imediatamente em frente ao edifício
principal e de frente para ele, é uma estátua de cobre de Cristo com os braços erguidos com a
lenda &quot;Venite Ad Me Omnes&quot;. Ao lado do edifício principal é a Basílica do Sagrado
Coração. Imediatamente atrás da basílica é a Gruta, um lugar mariano de oração e reflexão.
É uma réplica da gruta em Lourdes, na França, onde a Virgem Maria supostamente apareceu a Santa
Bernadette Soubirous em 1858. No final da unidade principal (e em uma linha direta que liga
através de 3 estátuas e da Cúpula de Ouro), é um estátua de pedra simples e moderna de Maria."""

question = 'A quem a Virgem Maria supostamente apareceu em 1858 em Lourdes, na França?'
```

```
python
>>> ptnet.query(context=context, question=question)
'Santa Bernadette Soubirous'
```

```
python
context = """Beyoncé Giselle Knowles-Carter (nascida em 4 de setembro de 1981) é uma cantora
americana, compositora, produtora de discos e atriz. Nascida e criada em Houston, Texas, ela se
apresentou em várias competições de canto e dança quando criança, e alcançou a fama no final dos
anos 90 como vocalista do grupo de R &amp; B Destiny&#39;s Child. Dirigida por seu pai, Mathew
Knowles, o grupo tornou-se um dos grupos femininos mais vendidos de todos os tempos. Seu hiato
viu o lançamento do álbum de estreia de Beyoncé, Dangerously in Love (2003), que a consagrou como
artista solo em todo o mundo, ganhou cinco prêmios Grammy e apresentou os singles número um da
Billboard Hot 100 &quot;Crazy in Love&quot; e &quot;Baby Boy&quot; ."""

question = 'Em que cidade e estado Beyonce cresceu?'
```

```
python
>>> ptnet.query(context=context, question=question)
'Houston, Texas'
```

```
python
context = """Em 17 de Outubro desse ano, a Comissão da Administração dos Bens pertencentes ao
Estado inquire junto da Sociedade Martins Sarmento se o seu edifício se encontra em condições de
segurança tais que possa, sem perigo, receber e conservar em exposição os objectos de valor
histórico e artístico correspondente ao chamado Tesouro da Colegiada de Guimarães. Poucos dias
depois, a 28 do mesmo mês, a Delegação da Procuradoria da República, em Guimarães, informava que
o Ministro da Instrução, concordando com o parecer da Comissão Jurisdicional, autorizou que
fossem entregues, mediante rigoroso inventário, a essa Sociedade os móveis de carácter histórico
ou artístico arrolados nos edifícios das extintas congregações religiosas desta cidade. No
entanto, o Arquivo só nasceria em 1931, através decreto nº 19.952, de 27 de Junho do dito ano."""

question = 'Em que ano nasceu o arquivo?'
```

```
python
>>> ptnet.query(context=context, question=question)
'1931'
```

## Using the qaptnet API

`qaptnet-api.py` provides a simple interface to the model via HTTP. Once all the
requirements are met you can run it by simply executing:

    $ python qaptnet-api

The API is available on port `http://localhost:7788`, we can query the model via HTTP, for example
using  `curl`:

    $ cat data.json
    {"context": "Arquitetonicamente, a escola tem um caráter católico. (...), "question": "A quem
    a Virgem Maria supostamente apareceu em 1858 em Lourdes, na França?"}
    $ curl -H "Content-Type: application/json" \
           --data @data.json \
           http://localhost:7788/query
    {"answer":"Santa Bernadette Soubirous"}

A Docker file is also available, to build the Docker image run:

    $ docker build -t qaptnet-api:latest .

And run the container:

    $ docker run -d --rm -p 7788:7788 qaptnet-api

Again, the API is available in `http://localhost:7788`, and the same method illustrated before
can be used to query the model.

## Acknowledgements

This work is partially supported by the project “SmartEGOV: Harnessing EGOV for Smart Governance (Foundations, methods, Tools) / NORTE-01-0145-FEDER-000037”,
supported by Norte Portugal Regional Operational Programme (NORTE 2020),
under the PORTUGAL 2020 Partnership Agreement, through the European Regional
Development Fund (EFDR).

