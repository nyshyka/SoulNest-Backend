"""For You Section endpoints"""
from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from app.db.session import get_db
from app.models.new_models import QuizResult, MoodEntry, CalendarEntry, JournalEntry
from app.models import User
from app.schemas.new_schemas import (
    QuizResultCreate, MoodEntryCreate, MoodEntryPublic,
    CalendarEntryCreate, CalendarEntryPublic,
    JournalEntryCreate, JournalEntryPublic
)
from .deps import get_current_user


router = APIRouter(prefix="/api/for-you", tags=["for-you"])


@router.post("/quiz-results", status_code=201)
async def save_quiz_result(
    payload: QuizResultCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save quiz result"""
    result = QuizResult(
        user_id=current_user.id,
        answers=payload.answers,
        recommended_ritual_id=payload.recommended_ritual_id
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


@router.post("/mood-entries", response_model=MoodEntryPublic, status_code=201)
async def save_mood_entry(
    payload: MoodEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save mood entry"""
    entry_date = payload.date or date.today()
    # Check if entry exists for this date
    existing = await db.execute(
        select(MoodEntry).where(
            MoodEntry.user_id == current_user.id,
            MoodEntry.entry_date == entry_date
        )
    )
    entry = existing.scalar_one_or_none()
    if entry:
        entry.mood = payload.mood
        entry.note = payload.note
    else:
        entry = MoodEntry(
            user_id=current_user.id,
            mood=payload.mood,
            note=payload.note,
            entry_date=entry_date
        )
        db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.get("/mood-entries", response_model=List[MoodEntryPublic])
async def get_mood_entries(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get mood entries"""
    stmt = select(MoodEntry).where(MoodEntry.user_id == current_user.id)
    if start_date:
        stmt = stmt.where(MoodEntry.entry_date >= start_date)
    if end_date:
        stmt = stmt.where(MoodEntry.entry_date <= end_date)
    stmt = stmt.order_by(MoodEntry.entry_date.desc())
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/calendar-entries", response_model=CalendarEntryPublic, status_code=201)
async def save_calendar_entry(
    payload: CalendarEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save calendar entry"""
    existing = await db.execute(
        select(CalendarEntry).where(
            CalendarEntry.user_id == current_user.id,
            CalendarEntry.entry_date == payload.date
        )
    )
    entry = existing.scalar_one_or_none()
    if entry:
        entry.ritual_completed = payload.ritual_completed
        entry.notes = payload.notes
    else:
        entry = CalendarEntry(
            user_id=current_user.id,
            entry_date=payload.date,
            ritual_completed=payload.ritual_completed,
            notes=payload.notes
        )
        db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.get("/calendar-entries", response_model=List[CalendarEntryPublic])
async def get_calendar_entries(
    month: str = Query(..., description="YYYY-MM"),
    year: int = Query(..., description="YYYY"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get calendar entries for a month"""
    from calendar import monthrange
    start_date = date(year, int(month.split("-")[1]), 1)
    last_day = monthrange(year, int(month.split("-")[1]))[1]
    end_date = date(year, int(month.split("-")[1]), last_day)

    stmt = select(CalendarEntry).where(
        CalendarEntry.user_id == current_user.id,
        CalendarEntry.entry_date >= start_date,
        CalendarEntry.entry_date <= end_date
    ).order_by(CalendarEntry.entry_date.asc())
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/journal-entries", response_model=JournalEntryPublic, status_code=201)
async def save_journal_entry(
    payload: JournalEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save journal entry"""
    entry_date = payload.date or date.today()
    entry = JournalEntry(
        user_id=current_user.id,
        content=payload.content,
        entry_date=entry_date
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.get("/journal-entries", response_model=List[JournalEntryPublic])
async def get_journal_entries(
    limit: Optional[int] = Query(10),
    offset: Optional[int] = Query(0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get journal entries"""
    stmt = select(JournalEntry).where(
        JournalEntry.user_id == current_user.id
    ).order_by(JournalEntry.entry_date.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

