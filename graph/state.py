from typing import TypedDict, List, Dict, Any

class CandidateSession(TypedDict):
    name: str
    difficulty: int
    resume: str
    jd: str

class AgentEvaluation(TypedDict):
    tech_score: float
    tech_feedback: str
    comm_score: float
    comm_feedback: str
    verifier_score: float
    verifier_feedback: str
    perfected_phrase: str
    ideal_tech: float
    ideal_comm: float
    ideal_verifier: float

class InterviewState(TypedDict):
    session: CandidateSession
    questions: List[Dict[str, str]]
    evaluations: List[AgentEvaluation]
    current_q_index: int
    quiz_passed: bool
