import json
from typing import Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from constants import Constants
from utils import read_prompt_from_file

class IntentIdentifierService:
    def __init__(self, openai_api_key: str):
        self.__llm_chain = ChatOpenAI(
            model=Constants.INTENT_IDENTIFIER_GPT_MODEL, 
            api_key=openai_api_key
        )

    def invoke(self, user_text) -> Any:
        messages = self.__get_llm_messages(user_text)
        output = self.__llm_chain.invoke(messages)
        return json.loads(output.content)

    def __get_llm_messages(self, user_text) -> List[BaseMessage]:
        return [
            self.__get_system_message(),
            self.__get_human_message(user_text)
        ]

    def __get_system_message(self) -> SystemMessage:
        return SystemMessage(content=read_prompt_from_file(Constants.INTENT_IDENTIFIER_SYS_MSG_FILE_NAME))

    def __get_human_message(self, user_text) -> HumanMessage:
        return HumanMessage(content=user_text)
