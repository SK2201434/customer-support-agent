from app.llm.provider import get_llm


def test_llm_creation():
    llm = get_llm()

    assert llm is not None
    assert llm.model == "qwen3:8b"