# AI 에게 질문하고 답을 만듭니다.

from app.ai import llm, masking, prompts
from app.rag.reranker import rerank
from app.rag.retriever import retrieve

# 후보를 넉넉히 뽑아야 리랭커가 고를 것이 생깁니다.
#
# "건성 피부에 쓸 토너" 로 후보 10개를 뽑아 보니 9개가 전부 "사용법" 섹션이었습니다.
# 리랭커는 검색이 안 가져온 글을 만들어내지 못하므로, 이때는 아무리 잘 골라도 소용이 없습니다.
# 20개로 넓히니 "이런 분께 권합니다", "후기" 같은 다른 섹션이 섞여 들어왔고,
# 리랭커가 실제 토너 상품 세 개를 골라냈습니다.
CANDIDATES = 20
TOP_K = 4


def ask(db, question):
    candidates = retrieve(db, question, CANDIDATES)
    chunks = rerank(question, candidates, TOP_K)
    chunks = masking.mask_chunks(chunks)

    user_prompt = prompts.build_rag_prompt(question, chunks)
    answer = llm.ask(prompts.RAG_SYSTEM, user_prompt)

    return {"question": question, "answer": answer, "sources": chunks}