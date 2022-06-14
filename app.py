from elg import FlaskService
from elg.model import AnnotationsResponse, Failure
from elg.model.base import StandardMessages

from keras_bert_ner.serve import Tagger
from utils import iob2_to_elg

MODEL_DIR = 'keras_bert_ner/ner-model'


class FinBertNer(FlaskService):

    tagger = Tagger.load(MODEL_DIR)

    def convert_to_elg(self, content, ner_res):
        annotations = {}
        entities = iob2_to_elg(content, ner_res)
        for entity in entities:
            label, annot = entity
            annotations.setdefault(label, []).append(annot)
        try:
            return AnnotationsResponse(annotations=annotations)
        except Exception as err:
            error_msg = StandardMessages.\
                    generate_elg_service_internalerror(params=[str(err)])
            return Failure(errors=[error_msg])

    def process_text(self, content):
        ner_res = self.tagger.tag(content.content, False)
        return self.convert_to_elg(content.content, ner_res)


flask_service = FinBertNer("FinBERTNER")
app = flask_service.app
