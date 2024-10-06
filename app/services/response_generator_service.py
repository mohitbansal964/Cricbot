import json
from typing import Any, List
from langchain_openai import ChatOpenAI
from constants import Constants
from models import MatchDetails
from utils import read_prompt_from_file
from langchain.prompts import PromptTemplate

class ResponseGeneratorService:
    def __init__(self, openai_api_key: str):
        self.__llm_chain = ChatOpenAI(
            model=Constants.RESPONSE_GENERATOR_GPT_MODEL, 
            api_key=openai_api_key
        )

    def get_live_score_response(self, user_input: str, match_details: MatchDetails) -> str:
        prompt = self.__get_live_score_prompt(user_input, match_details)
        output = self.__llm_chain.invoke(prompt)
        return output.content
    
    def get_fallback_response(self, user_input: str, reason: str) -> str:
        prompt = self.__get_fallback_prompt(user_input, reason)
        output = self.__llm_chain.invoke(prompt)
        return output.content

    def __get_live_score_prompt(self, user_input: str, match_details: MatchDetails) -> str:
        prompt_template = self.__get_live_score_prompt_template()
        prompt = prompt_template.format(
            user_input=user_input,
            t1_name=match_details.team_1.name,
            t1_abr=match_details.team_1.abr,
            t1_run=match_details.team_1.run,
            t1_wkt=match_details.team_1.wicket,
            t1_ovr=match_details.team_1.over,
            t2_name=match_details.team_2.name,
            t2_abr=match_details.team_2.abr,
            t2_run=match_details.team_2.run,
            t2_wkt=match_details.team_2.wicket,
            t2_ovr=match_details.team_2.over,
            status=match_details.status
        )
        return prompt

    def __get_live_score_prompt_template(self) -> PromptTemplate:
        return PromptTemplate.from_template(
            template=read_prompt_from_file(Constants.LIVE_SCORE_RESPONSE_PROMPT)
        )
    
    def __get_fallback_prompt(self, user_input: str, reason: str) -> str:
        prompt_template = self.__get_fallback_prompt_template()
        prompt = prompt_template.format(
            user_input=user_input,
            reason=reason
        )
        return prompt

    def __get_fallback_prompt_template(self) -> PromptTemplate:
        return PromptTemplate.from_template(
            template=read_prompt_from_file(Constants.FALLBACK_RESPONSE_PROMPT)
        )
    
