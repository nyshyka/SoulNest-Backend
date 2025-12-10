import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models import User
from app.utils.security import hash_password


async def seed_users(session: AsyncSession) -> None:
    defaults = [
        {
            "name": "Learner",
            "email": "learner@soulnest.com",
            "password": "learning123",
            "is_guest": False,
        },
        {
            "name": "Guest",
            "email": "guest@example.com",
            "password": "guest",
            "is_guest": True,
        },
    ]

    for u in defaults:
        result = await session.execute(select(User).where(User.email == u["email"]))
        existing = result.scalar_one_or_none()
        if existing:
            continue
        user = User(
            name=u["name"],
            email=u["email"],
            password_hash=hash_password(u["password"]),
            is_guest=u["is_guest"],
        )
        session.add(user)
    await session.commit()


async def main() -> None:
    async with AsyncSessionLocal() as session:
        await seed_users(session)
    print("✓ Seeded default users (if missing).")


if __name__ == "__main__":
    asyncio.run(main())


