from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class IntPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class Base(DeclarativeBase, IntPkMixin):
    pass

