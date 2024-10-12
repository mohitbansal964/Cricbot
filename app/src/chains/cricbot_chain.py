from src.services import IntentHandlerService, ResponseGeneratorService, LiveMatchService, IntentIdentifierService
from src.utils import get_live_matches_as_string
from src.models import IntentDetails
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

def generate_chain(openai_api_key: str, metadata: dict):
    intent_identifier_service = IntentIdentifierService(openai_api_key)
    response_generator_service = ResponseGeneratorService(openai_api_key)
    intent_handler_service = IntentHandlerService()
    json_parser = JsonOutputParser(pydantic_object=IntentDetails)
    str_parser = StrOutputParser()
    chain = (lambda x: {**metadata, "live_matches": get_live_matches_as_string(LiveMatchService().fetch_all_matches())}) \
        | intent_identifier_service.get_chat_prompt_template(json_parser) \
        | intent_identifier_service.llm \
        | json_parser \
        | intent_handler_service.get_addtional_data \
        | (lambda data: {**metadata, **data}) \
        | response_generator_service.get_prompt \
        | response_generator_service.llm \
        | str_parser
    return chain


