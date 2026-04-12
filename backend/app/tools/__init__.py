from enum import Enum
from functools import lru_cache
from typing import Annotated, Literal

from langchain.tools.retriever import create_retriever_tool
from langchain_community.agent_toolkits.connery import ConneryToolkit
from langchain_community.retrievers.kay import KayAiRetriever
from langchain_community.retrievers.pubmed import PubMedRetriever
from langchain_community.retrievers.wikipedia import WikipediaRetriever
from langchain_community.retrievers.you import YouRetriever
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.connery import ConneryService
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import (
    TavilyAnswer as _TavilyAnswer,
)
from langchain_community.tools.tavily_search import (
    TavilySearchResults,
)
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.tools import StructuredTool, Tool
from pydantic import BaseModel, Field
from typing_extensions import NotRequired, TypedDict

from app.tools.news_articles import get_news_articles
from app.tools.student_activities import get_student_activities
from app.tools.timetable import get_timetable
from app.tools.user_profile import get_user_profile
from app.upload import vstore


class DDGInput(BaseModel):
    query: Annotated[str, Field(description="search query to look up")]


class ArxivInput(BaseModel):
    query: Annotated[str, Field(description="search query to look up")]


class PythonREPLInput(BaseModel):
    query: Annotated[str, Field(description="python command to run")]


class DallEInput(BaseModel):
    query: Annotated[str, Field(description="image description to generate image from")]


class NewsArticlesInput(BaseModel):
    query: Annotated[str, Field(description="search query to look up")]


class StudentActivitiesInput(BaseModel):
    keyword: Annotated[
        str | None,
        Field(default=None, description="optional keyword to search student activities"),
    ]
    activity_type: Annotated[
        str | None,
        Field(default=None, description="optional activity type filter"),
    ]
    campus_id: Annotated[
        int | None,
        Field(default=None, description="optional campus ID filter"),
    ]
    discipline: Annotated[
        str | None,
        Field(default=None, description="optional discipline filter"),
    ]
    locale: Annotated[
        str | None,
        Field(default=None, description="optional locale filter, for example en or zh-HK"),
    ]
    limit: Annotated[
        int | None,
        Field(default=None, description="optional max number of results (1-20)"),
    ]


class TimetableInput(BaseModel):
    start_date: Annotated[
        str | None,
        Field(default=None, description="optional start date in YYYY-MM-DD format"),
    ]
    end_date: Annotated[
        str | None,
        Field(default=None, description="optional end date in YYYY-MM-DD format"),
    ]


class AvailableTools(str, Enum):
    ACTION_SERVER = "action_server_by_sema4ai"
    CONNERY = "ai_action_runner_by_connery"
    DDG_SEARCH = "ddg_search"
    TAVILY = "search_tavily"
    TAVILY_ANSWER = "search_tavily_answer"
    RETRIEVAL = "retrieval"
    ARXIV = "arxiv"
    YOU_SEARCH = "you_search"
    SEC_FILINGS = "sec_filings_kai_ai"
    PRESS_RELEASES = "press_releases_kai_ai"
    PUBMED = "pubmed"
    WIKIPEDIA = "wikipedia"
    DALL_E = "dall_e"
    NEWS_ARTICLES = "news_articles"
    STUDENT_ACTIVITIES = "student_activities"
    USER_PROFILE = "user_profile"
    TIMETABLE = "timetable"


class ToolConfig(TypedDict):
    ...


class BaseTool(BaseModel):
    type: AvailableTools
    name: str
    description: str
    config: ToolConfig = Field(default_factory=dict)
    multi_use: bool = False


class ActionServerConfig(ToolConfig):
    url: str
    api_key: str


class UserProfileConfig(ToolConfig):
    user_id: str
    locale: NotRequired[str]


class TimetableConfig(ToolConfig):
    user_id: str


class ActionServer(BaseTool):
    type: Literal[AvailableTools.ACTION_SERVER] = AvailableTools.ACTION_SERVER
    name: Literal["Action Server by Sema4.ai"] = "Action Server by Sema4.ai"
    description: Literal[
        (
            "Run AI actions with "
            "[Sema4.ai Action Server](https://github.com/Sema4AI/actions)."
        )
    ] = (
        "Run AI actions with "
        "[Sema4.ai Action Server](https://github.com/Sema4AI/actions)."
    )
    config: ActionServerConfig
    multi_use: Literal[True] = True


class Connery(BaseTool):
    type: Literal[AvailableTools.CONNERY] = AvailableTools.CONNERY
    name: Literal["AI Action Runner by Connery"] = "AI Action Runner by Connery"
    description: Literal[
        (
            "Connect OpenGPTs to the real world with "
            "[Connery](https://github.com/connery-io/connery)."
        )
    ] = (
        "Connect OpenGPTs to the real world with "
        "[Connery](https://github.com/connery-io/connery)."
    )


class DDGSearch(BaseTool):
    type: Literal[AvailableTools.DDG_SEARCH] = AvailableTools.DDG_SEARCH
    name: Literal["DuckDuckGo Search"] = "DuckDuckGo Search"
    description: Literal[
        "Search the web with [DuckDuckGo](https://pypi.org/project/duckduckgo-search/)."
    ] = "Search the web with [DuckDuckGo](https://pypi.org/project/duckduckgo-search/)."


class Arxiv(BaseTool):
    type: Literal[AvailableTools.ARXIV] = AvailableTools.ARXIV
    name: Literal["Arxiv"] = "Arxiv"
    description: Literal[
        "Searches [Arxiv](https://arxiv.org/)."
    ] = "Searches [Arxiv](https://arxiv.org/)."


class YouSearch(BaseTool):
    type: Literal[AvailableTools.YOU_SEARCH] = AvailableTools.YOU_SEARCH
    name: Literal["You.com Search"] = "You.com Search"
    description: Literal[
        "Uses [You.com](https://you.com/) search, optimized responses for LLMs."
    ] = "Uses [You.com](https://you.com/) search, optimized responses for LLMs."


class SecFilings(BaseTool):
    type: Literal[AvailableTools.SEC_FILINGS] = AvailableTools.SEC_FILINGS
    name: Literal["SEC Filings (Kay.ai)"] = "SEC Filings (Kay.ai)"
    description: Literal[
        "Searches through SEC filings using [Kay.ai](https://www.kay.ai/)."
    ] = "Searches through SEC filings using [Kay.ai](https://www.kay.ai/)."


class PressReleases(BaseTool):
    type: Literal[AvailableTools.PRESS_RELEASES] = AvailableTools.PRESS_RELEASES
    name: Literal["Press Releases (Kay.ai)"] = "Press Releases (Kay.ai)"
    description: Literal[
        "Searches through press releases using [Kay.ai](https://www.kay.ai/)."
    ] = "Searches through press releases using [Kay.ai](https://www.kay.ai/)."


class PubMed(BaseTool):
    type: Literal[AvailableTools.PUBMED] = AvailableTools.PUBMED
    name: Literal["PubMed"] = "PubMed"
    description: Literal[
        "Searches [PubMed](https://pubmed.ncbi.nlm.nih.gov/)."
    ] = "Searches [PubMed](https://pubmed.ncbi.nlm.nih.gov/)."


class Wikipedia(BaseTool):
    type: Literal[AvailableTools.WIKIPEDIA] = AvailableTools.WIKIPEDIA
    name: Literal["Wikipedia"] = "Wikipedia"
    description: Literal[
        "Searches [Wikipedia](https://pypi.org/project/wikipedia/)."
    ] = "Searches [Wikipedia](https://pypi.org/project/wikipedia/)."


class Tavily(BaseTool):
    type: Literal[AvailableTools.TAVILY] = AvailableTools.TAVILY
    name: Literal["Search (Tavily)"] = "Search (Tavily)"
    description: Literal[
        (
            "Uses the [Tavily](https://app.tavily.com/) search engine. "
            "Includes sources in the response."
        )
    ] = (
        "Uses the [Tavily](https://app.tavily.com/) search engine. "
        "Includes sources in the response."
    )


class TavilyAnswer(BaseTool):
    type: Literal[AvailableTools.TAVILY_ANSWER] = AvailableTools.TAVILY_ANSWER
    name: Literal["Search (short answer, Tavily)"] = "Search (short answer, Tavily)"
    description: Literal[
        (
            "Uses the [Tavily](https://app.tavily.com/) search engine. "
            "This returns only the answer, no supporting evidence."
        )
    ] = (
        "Uses the [Tavily](https://app.tavily.com/) search engine. "
        "This returns only the answer, no supporting evidence."
    )


class Retrieval(BaseTool):
    type: Literal[AvailableTools.RETRIEVAL] = AvailableTools.RETRIEVAL
    name: Literal["Retrieval"] = "Retrieval"
    description: Literal[
        "Look up information in uploaded files."
    ] = "Look up information in uploaded files."


class DallE(BaseTool):
    type: Literal[AvailableTools.DALL_E] = AvailableTools.DALL_E
    name: Literal["Generate Image (Dall-E)"] = "Generate Image (Dall-E)"
    description: Literal[
        "Generates images from a text description using OpenAI's DALL-E model."
    ] = "Generates images from a text description using OpenAI's DALL-E model."


class NewsArticles(BaseTool):
    type: Literal[AvailableTools.NEWS_ARTICLES] = AvailableTools.NEWS_ARTICLES
    name: Literal["News Articles"] = "News Articles"
    description: Literal[
        "Retrieve latest news and announcements by the Vocational Training Council (VTC) and its member institutions."
    ] = "Retrieve latest news and announcements by the Vocational Training Council (VTC) and its member institutions."


class StudentActivities(BaseTool):
    type: Literal[AvailableTools.STUDENT_ACTIVITIES] = AvailableTools.STUDENT_ACTIVITIES
    name: Literal["Student Activities"] = "Student Activities"
    description: Literal[
        "Retrieve active and upcoming student activities from the MyPortal backend by keyword and filters."
    ] = "Retrieve active and upcoming student activities from the MyPortal backend by keyword and filters."


class UserProfile(BaseTool):
    type: Literal[AvailableTools.USER_PROFILE] = AvailableTools.USER_PROFILE
    name: Literal["User Profile"] = "User Profile"
    description: Literal[
        "Retrieve the configured user's profile from the MyPortal backend."
    ] = "Retrieve the configured user's profile from the MyPortal backend."
    config: UserProfileConfig


class Timetable(BaseTool):
    type: Literal[AvailableTools.TIMETABLE] = AvailableTools.TIMETABLE
    name: Literal["Timetable"] = "Timetable"
    description: Literal[
        "Retrieve the configured user's timetable events and holiday from the MyPortal backend."
    ] = "Retrieve the configured user's timetable events and holiday from the MyPortal backend."
    config: TimetableConfig


RETRIEVAL_DESCRIPTION = """Can be used to look up information that was uploaded to this assistant.
If the user is referencing particular files, that is often a good hint that information may be here.
If the user asks a vague question, they are likely meaning to look up info from this retriever, and you should call it!"""


def get_retriever(assistant_id: str, thread_id: str):
    return vstore.as_retriever(
        search_kwargs={"filter": {"namespace": {"$in": [assistant_id, thread_id]}}}
    )


@lru_cache(maxsize=5)
def get_retrieval_tool(assistant_id: str, thread_id: str, description: str):
    return create_retriever_tool(
        get_retriever(assistant_id, thread_id),
        "Retriever",
        description,
    )


@lru_cache(maxsize=1)
def _get_duck_duck_go():
    return DuckDuckGoSearchRun(args_schema=DDGInput)


@lru_cache(maxsize=1)
def _get_arxiv():
    return ArxivQueryRun(api_wrapper=ArxivAPIWrapper(), args_schema=ArxivInput)


@lru_cache(maxsize=1)
def _get_you_search():
    return create_retriever_tool(
        YouRetriever(n_hits=3, n_snippets_per_hit=3),
        "you_search",
        "Searches for documents using You.com",
    )


@lru_cache(maxsize=1)
def _get_sec_filings():
    return create_retriever_tool(
        KayAiRetriever.create(
            dataset_id="company", data_types=["10-K", "10-Q"], num_contexts=3
        ),
        "sec_filings_search",
        "Search for a query among SEC Filings",
    )


@lru_cache(maxsize=1)
def _get_press_releases():
    return create_retriever_tool(
        KayAiRetriever.create(
            dataset_id="company", data_types=["PressRelease"], num_contexts=6
        ),
        "press_release_search",
        "Search for a query among press releases from US companies",
    )


@lru_cache(maxsize=1)
def _get_pubmed():
    return create_retriever_tool(
        PubMedRetriever(), "pub_med_search", "Search for a query on PubMed"
    )


@lru_cache(maxsize=1)
def _get_wikipedia():
    return create_retriever_tool(
        WikipediaRetriever(), "wikipedia", "Search for a query on Wikipedia"
    )


@lru_cache(maxsize=1)
def _get_tavily():
    tavily_search = TavilySearchAPIWrapper()
    return TavilySearchResults(api_wrapper=tavily_search, name="search_tavily")


@lru_cache(maxsize=1)
def _get_tavily_answer():
    tavily_search = TavilySearchAPIWrapper()
    return _TavilyAnswer(api_wrapper=tavily_search, name="search_tavily_answer")


@lru_cache(maxsize=1)
def _get_connery_actions():
    connery_service = ConneryService()
    connery_toolkit = ConneryToolkit.create_instance(connery_service)
    tools = connery_toolkit.get_tools()
    return tools


@lru_cache(maxsize=1)
def _get_dalle_tools():
    return Tool(
        "Dall-E-Image-Generator",
        DallEAPIWrapper(size="1024x1024", quality="hd").run,
        "A wrapper around OpenAI DALL-E API. Useful for when you need to generate images from a text description. Input should be an image description.",
    )


@lru_cache(maxsize=5)
def _get_news_articles():
    return Tool(
        "news_articles",
        get_news_articles,
        "Retrieve latest VTC news and announcements by keyword from the MyPortal backend.",
        args_schema=NewsArticlesInput,
    )


@lru_cache(maxsize=5)
def _get_student_activities():
    return StructuredTool.from_function(
        func=get_student_activities,
        name="student_activities",
        description="Retrieve active and upcoming student activities by keyword and optional filters from the MyPortal backend.",
        args_schema=StudentActivitiesInput,
    )


@lru_cache(maxsize=256)
def _get_user_profile(user_id: str, locale: str | None = None):
    return Tool(
        "user_profile",
        lambda _tool_input="": get_user_profile(user_id=user_id, locale=locale),
        description="Retrieve the current user's profile from MyPortal.",
    )


@lru_cache(maxsize=256)
def _get_timetable(user_id: str):
    return StructuredTool.from_function(
        func=lambda start_date=None, end_date=None: get_timetable(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        ),
        name="timetable",
        description="Retrieve the current user's timetable events and holiday from MyPortal.",
        args_schema=TimetableInput,
    )


TOOLS = {
    AvailableTools.CONNERY: _get_connery_actions,
    AvailableTools.DDG_SEARCH: _get_duck_duck_go,
    AvailableTools.ARXIV: _get_arxiv,
    AvailableTools.YOU_SEARCH: _get_you_search,
    AvailableTools.SEC_FILINGS: _get_sec_filings,
    AvailableTools.PRESS_RELEASES: _get_press_releases,
    AvailableTools.PUBMED: _get_pubmed,
    AvailableTools.TAVILY: _get_tavily,
    AvailableTools.WIKIPEDIA: _get_wikipedia,
    AvailableTools.TAVILY_ANSWER: _get_tavily_answer,
    AvailableTools.DALL_E: _get_dalle_tools,
    AvailableTools.NEWS_ARTICLES: _get_news_articles,
    AvailableTools.STUDENT_ACTIVITIES: _get_student_activities,
    AvailableTools.USER_PROFILE: _get_user_profile,
    AvailableTools.TIMETABLE: _get_timetable,
}
