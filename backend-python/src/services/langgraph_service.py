from __future__ import annotations

from typing import Any, Dict, TypedDict, Literal

from langgraph.graph import StateGraph, END

from src.services.llm_service import get_keyword_response, generate_response
from src.services.rag_service import generate_rag_response, is_rag_initialized


class GraphState(TypedDict, total=False):
    prompt: str
    clean_prompt: str
    user_id: str
    language: str
    max_tokens: int
    temperature: float
    response: str
    source: str
    tokens_used: int
    documents: list
    intent: str
    category: str


def _normalize_input(state: GraphState) -> Dict[str, Any]:
    prompt = (state.get("prompt") or "").strip()
    return {"clean_prompt": prompt}


def _keyword_check(state: GraphState) -> Dict[str, Any]:
    prompt = state.get("prompt", "")
    language = state.get("language", "ko")
    resp = get_keyword_response(prompt, language)
    if not resp:
        print("[LangGraph] keyword: miss -> rag")
        return {"intent": "classify"}
    print("[LangGraph] keyword: hit")
    return {
        "intent": "keyword",
        "response": resp.get("response", ""),
        "source": resp.get("source", "keyword"),
        "tokens_used": resp.get("tokens_used", 0),
    }


def _classify_question(state: GraphState) -> Dict[str, Any]:
    question = (state.get("prompt") or "").lower()
    school_keywords = [
        "학과", "학과소개", "모집", "입학", "서류", "전형", "면접", "필기",
        "교육비", "훈련", "장려금", "취업", "취업현황", "교학처", "연락처",
        "위치", "주소", "주차", "식당", "캠퍼스", "교수", "교수님",
        "수료", "과정", "커리큘럼", "수강", "모집요강"
    ]
    if any(k in question for k in school_keywords):
        print("[LangGraph] classify: school -> rag")
        return {"category": "school"}
    print("[LangGraph] classify: general -> llm")
    return {"category": "general"}


def _rag_answer(state: GraphState) -> Dict[str, Any]:
    if not is_rag_initialized():
        print("[LangGraph] rag: not initialized -> llm fallback")
        return {"intent": "llm_fallback"}
    query = state.get("prompt", "")
    language = state.get("language", "ko")
    print("[LangGraph] rag: search start")
    result = generate_rag_response(query=query, language=language, k=3)
    source = result.get("source", "")
    response = result.get("response", "")
    updates: Dict[str, Any] = {
        "response": response,
        "source": source,
        "tokens_used": result.get("tokens_used", 0),
        "documents": result.get("documents", []),
    }
    if source == "none" or not response:
        print("[LangGraph] rag: no answer -> llm fallback")
        updates["intent"] = "llm_fallback"
    else:
        print(f"[LangGraph] rag: ok docs={len(updates.get('documents', []))}")
    return updates


def _llm_answer(state: GraphState) -> Dict[str, Any]:
    prompt = state.get("prompt", "")
    language = state.get("language", "ko")
    user_id = state.get("user_id", "default")
    max_tokens = int(state.get("max_tokens") or 256)
    temperature = float(state.get("temperature") or 0.7)
    print("[LangGraph] llm: start")
    result = generate_response(
        prompt=prompt,
        user_id=user_id,
        max_tokens=max_tokens,
        temperature=temperature,
        language=language,
    )
    print("[LangGraph] llm: done")
    return {
        "response": result.get("response", ""),
        "source": result.get("source", "llm"),
        "tokens_used": result.get("tokens_used", 0),
    }


def _route_after_keyword(state: GraphState) -> Literal["keyword", "classify"]:
    intent = state.get("intent", "")
    if intent == "keyword":
        return "keyword"
    return "classify"


def _route_after_classify(state: GraphState) -> Literal["rag", "llm"]:
    if state.get("category") == "school":
        return "rag"
    return "llm"


def _route_after_rag(state: GraphState) -> Literal["end", "llm"]:
    if state.get("intent") == "llm_fallback":
        return "llm"
    return "end"


def _route_after_keyword(state: GraphState) -> Literal["keyword", "rag", "llm"]:
    intent = state.get("intent", "")
    if intent == "keyword":
        return "keyword"
    return "rag" if is_rag_initialized() else "llm"


def _route_after_rag(state: GraphState) -> Literal["end", "llm"]:
    if state.get("intent") == "llm_fallback":
        return "llm"
    return "end"


def _build_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("normalize", _normalize_input)
    workflow.add_node("keyword_check", _keyword_check)
    workflow.add_node("classify", _classify_question)
    workflow.add_node("rag_answer", _rag_answer)
    workflow.add_node("llm_answer", _llm_answer)

    workflow.set_entry_point("normalize")
    workflow.add_edge("normalize", "keyword_check")

    workflow.add_conditional_edges(
        "keyword_check",
        _route_after_keyword,
        {
            "keyword": END,
            "classify": "classify",
        },
    )

    workflow.add_conditional_edges(
        "classify",
        _route_after_classify,
        {
            "rag": "rag_answer",
            "llm": "llm_answer",
        },
    )

    workflow.add_conditional_edges(
        "rag_answer",
        _route_after_rag,
        {
            "end": END,
            "llm": "llm_answer",
        },
    )

    workflow.add_edge("llm_answer", END)
    return workflow.compile()


_GRAPH_APP = None


def get_graph_app():
    global _GRAPH_APP
    if _GRAPH_APP is None:
        _GRAPH_APP = _build_graph()
    return _GRAPH_APP


def invoke_graph(
    prompt: str,
    language: str = "ko",
    user_id: str = "default",
    max_tokens: int = 256,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    app = get_graph_app()
    state: GraphState = {
        "prompt": prompt,
        "language": language,
        "user_id": user_id,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    result = app.invoke(state)
    return {
        "response": result.get("response", ""),
        "tokens_used": result.get("tokens_used", 0),
        "model": "LANGGRAPH",
        "language": language,
        "source": result.get("source", "unknown"),
        "documents": result.get("documents", []),
        "user_id": user_id,
    }
