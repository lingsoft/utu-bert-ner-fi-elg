"""
Based on Jouni Luoma's bcr-ner-demo (tag-ner.py).
Unpublished https://github.com/jouniluoma (personal communication).
"""

def iob2_span_ends(curr_type, tag):
    if curr_type is None:
        return False
    elif tag == 'I-{}'.format(curr_type):
        return False
    elif tag == 'O' or tag[0] == 'B':
        return True
    else:
        # assert curr_type != tag[2:], 'internal error'
        return True    # non-IOB2 or tag sequence error


def iob2_span_starts(curr_type, tag):
    if tag == 'O':
        return False
    elif tag[0] == 'B':
        return True
    elif curr_type is None:
        return True    # non-IOB2 or tag sequence error
    else:
        # assert tag == 'I-{}'.format(curr_type), 'internal error'
        return False


def tags_to_spans(text, tokens, tags):
    spans = []
    offset, curr_type, start = 0, None, None
    # assert len(tokens) == len(tags)
    for token, tag in zip(tokens, tags):
        if iob2_span_ends(curr_type, tag):
            spans.append((curr_type, {"start": start, "end": offset}))
            curr_type, start = None, None
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if text[offset:offset+len(token)] != token:
            raise ValueError('text mismatch')
        if iob2_span_starts(curr_type, tag):
            curr_type, start = tag[2:], offset
        offset += len(token)
    if curr_type is not None:
        spans.append((curr_type, {"start": start, "end": offset}))
    return spans


def iob2_to_elg(text, ner_res):
    tokens = []
    tags = []
    for line in ner_res.splitlines():
        if line.strip():
            token, tag = line.split('\t')
            tokens.append(token)
            tags.append(tag.strip())
    entities = tags_to_spans(text, tokens, tags)
    return entities
