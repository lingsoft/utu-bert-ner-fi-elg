from elg import FlaskService
from elg.model import TextRequest, AnnotationsResponse, Failure
from elg.model.base import StandardMessages

from keras_bert_ner.serve import Tagger
from utils import iob2_to_elg

MODEL_DIR = 'keras_bert_ner/ner-model'
MAX_CHAR = 30000


class FinBertNer(FlaskService):

    tagger = Tagger.load(MODEL_DIR)

    def convert_to_elg(self, content, ner_res):
        annotations = {}
        try:
            entities = iob2_to_elg(content, ner_res)
            for entity in entities:
                label, annot = entity
                annotations.setdefault(label, []).append(annot)
            return AnnotationsResponse(annotations=annotations)
        except Exception as err:
            error_msg = StandardMessages.\
                    generate_elg_service_internalerror(params=[str(err)])
            return Failure(errors=[error_msg])

    def process_text(self, request: TextRequest):
        content = request.content
        if len(content) > MAX_CHAR:
            error_msg = StandardMessages.generate_elg_request_too_large()
            return Failure(errors=[error_msg])
        try:
            ner_res = self.tagger.tag(content, False)
        except ValueError as err:
            error_msg = StandardMessages.\
                    generate_elg_service_internalerror(params=[str(err)])
            return Failure(errors=[error_msg])
        return self.convert_to_elg(content, ner_res)


flask_service = FinBertNer("FinBERTNER")
app = flask_service.app
