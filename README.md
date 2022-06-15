# ELG compatible FinBERT NER

## Information

TODO.

## Dependencies

### Python

Python < 3.8 and TensorFlow 1 (here cpu version is used). See 
[Issue #4](https://github.com/spyysalo/keras-bert-ner/issues/4) and
[fi-ner-eval](https://github.com/aajanki/fi-ner-eval#turku-ner).

### Model  

[Latest model](https://turkunlp.org/fin-ner.html) (combined-ext-model-130220.tar.gz) 
trained on Turku OntoNotes corpus is used.

## Quickstart

### Development

```
git clone --recurse-submodules https://github.com/lingsoft/utu-bert-ner-fi-elg.git
cd keras_bert_ner
./load-model.sh
cd ..
docker build -t finbert-ner-dev -f Dockerfile.dev .
docker run -it --rm -p 8000:8000 -v $(pwd):/app -u $(id -u):$(id -g) finbert-ner-dev bash
flask run --host 0.0.0.0 --port 8000
```

Simple test call (note slow startup time)

```
curl -X POST -H 'Content-Type: application/json' http://localhost:8000/process -d '{"type":"text","content":"Vuonna 1978 Pauli asui Turussa."}'
```

Response should be

```
{
  "response": {
    "type": "annotations",
    "annotations": {
      "DATE": [
        {
          "start": 0,
          "end": 11
        }
      ],
      "PERSON": [
        {
          "start": 12,
          "end": 17
        }
      ],
      "GPE": [
        {
          "start": 23,
          "end": 30
        }
      ]
    }
  }
}
```

### Tests

TODO.

### Usage

```
docker build -t finbert-ner .
docker run --rm -p 8000:8000 --init finbert-ner
```

### Local installation

Use ELG-compatible service locally

```
cd elg\_local && docker-compose up
```

The GUI is accessible on `http://localhost:5080`. See more 
[instructions](https://european-language-grid.readthedocs.io/en/stable/all/A1_PythonSDK/DeployServicesLocally.html#deploy-elg-compatible-service-from-its-docker-image)

## Next steps

- Each worker requires about 3.5GB memory. Option --preload has some 
  [issues](https://github.com/benoitc/gunicorn/issues/2369) with TensorFlow.
- For better performance [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)
  Convert hdf5 to savedModel format.
