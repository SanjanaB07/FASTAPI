from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal, Base
from auth import validate_auth

app = FastAPI()

Base.metadata.create_all(bind=engine)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# AUTH MIDDLEWARE
@app.middleware("http")
async def auth(request: Request, call_next):
    user = validate_auth(request)

    if not user:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    request.state.user = user
    return await call_next(request)


# ---------- AUTHORS ----------
@app.post("/authors")
def create_author(data: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create(db, models.Author(**data.dict()))


@app.get("/authors")
def list_authors(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Author)


# ---------- CATEGORIES ----------
@app.post("/categories")
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create(db, models.Category(**data.dict()))


@app.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Category)


# ---------- BOOKS ----------
@app.post("/books")
def create_book(data: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create(db, models.Book(**data.dict()))


@app.get("/books")
def list_books(db: Session = Depends(get_db)):
    return crud.get_all(db, models.Book)


@app.get("/books/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_by_id(db, models.Book, id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book


@app.delete("/books/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_by_id(db, models.Book, id)
    if not book:
        raise HTTPException(404, "Book not found")

    crud.delete(db, book)
    return {"message": "Deleted"}


# ---------- STATS ----------
@app.get("/stats/count")
def total_books(db: Session = Depends(get_db)):
    return {"total": db.query(models.Book).count()}


@app.get("/stats/average-year")
def avg_year(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    if not books:
        return {"average": 0}
    return {"average": sum(b.year for b in books)/len(books)}
