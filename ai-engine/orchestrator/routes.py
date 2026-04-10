from fastapi import APIRouter
from pydantic import BaseModel

from pipelines.lecture_pipeline.service import generate_slide_audio, generate_slides
from pipelines.podcast_pipeline.service import generate_dialogue, synthesize_turn
from pipelines.ppt_pipeline.service import generate_ppt
from pipelines.rag_pipeline.service import generate_flashcards

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


class LectureRequest(BaseModel):
    pdf_url: str
    title: str


class SlideAudioRequest(BaseModel):
    job_id: str
    slide_number: int
    text: str


class PodcastRequest(BaseModel):
    pdf_url: str


class TurnAudioRequest(BaseModel):
    job_id: str
    turn: int
    speaker: str
    text: str


class PPTRequest(BaseModel):
    job_id: str


class FlashcardRequest(BaseModel):
    pdf_url: str
    count: int = 20


@router.post("/lecture/slides")
async def lecture_slides(payload: LectureRequest):
    return await generate_slides(payload.pdf_url, payload.title)


@router.post("/lecture/slide-audio")
async def lecture_slide_audio(payload: SlideAudioRequest):
    return await generate_slide_audio(payload.job_id, payload.slide_number, payload.text)


@router.post("/lecture/ppt")
async def lecture_ppt(payload: PPTRequest):
    return await generate_ppt(payload.job_id)


@router.post("/podcast/dialogue")
async def podcast_dialogue(payload: PodcastRequest):
    return await generate_dialogue(payload.pdf_url)


@router.post("/podcast/turn-audio")
async def podcast_turn_audio(payload: TurnAudioRequest):
    return await synthesize_turn(payload.job_id, payload.turn, payload.speaker, payload.text)


@router.post("/rag/flashcards")
async def rag_flashcards(payload: FlashcardRequest):
    return await generate_flashcards(payload.pdf_url, payload.count)
