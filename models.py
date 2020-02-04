import pprint

from deeppavlov import configs, build_model
from pullenti_wrapper.processor import (
    Processor,
    DATE,
    GEO,
    ORGANIZATION,
    PERSON,
    MONEY,
    ADDRESS
)

pavlov_model = build_model(configs.ner.ner_rus, )

pullenti_processor = Processor([PERSON, ORGANIZATION, GEO, DATE, MONEY, ADDRESS])

def pavlov_entities(text):
    tokens, entities = pavlov_model([text])
    pairs = list(zip(tokens[0], entities[0]))
    pairs = filter(lambda el: el[1] != 'O', pairs)
    
    return '\n'.join(map(lambda el: ' - '.join(el), pairs))

def pullenti_entities(text):
    result = pullenti_processor(text)
    # for match in result.matches:
    #     print(match.referent.label, match.span)
    return pprint.pformat(result.matches, indent=2)
