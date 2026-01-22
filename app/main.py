from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
from .database import engine, create_db_and_tables, get_session
from .models import Post, Event, User, Comment, PostCreate, EventCreate, UserUpdate, CommentCreate, PostRead, EventRead, UserPostLike
import uuid
from sqlalchemy.orm import selectinload

app = FastAPI(title="Neighborly Connect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/posts", response_model=List[PostRead])
def read_posts(userId: str = None, session: Session = Depends(get_session)):
    posts = session.exec(select(Post).options(selectinload(Post.comments))).all()
    
    post_reads = []
    for post in posts:
        is_liked = False
        if userId:
            like = session.exec(select(UserPostLike).where(UserPostLike.userId == userId, UserPostLike.postId == post.id)).first()
            if like:
                is_liked = True
        
        post_read = PostRead.from_orm(post)
        post_read.isLiked = is_liked
        post_reads.append(post_read)
        
    return post_reads

@app.get("/events", response_model=List[EventRead])
def read_events(session: Session = Depends(get_session)):
    events = session.exec(select(Event).options(selectinload(Event.ageGroups))).all()
    return events

@app.get("/profile", response_model=User)
def read_profile(session: Session = Depends(get_session)):
    # Returning the default user for now
    user = session.exec(select(User).where(User.id == "user-1")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/")
def read_root():
    return {"message": "Welcome to Neighborly Connect API"}

@app.post("/posts", response_model=Post)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    author = session.get(User, post.authorId)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    new_post = Post(
        id=str(uuid.uuid4()),
        title=post.title,
        subtitle=post.subtitle,
        content=post.content,
        image=post.image,
        authorId=post.authorId,
        authorName=author.name,
        authorAvatar=author.avatar,
        likes=0
    )
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@app.get("/posts/{post_id}", response_model=PostRead)
def read_post(post_id: str, userId: str = None, session: Session = Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == post_id).options(selectinload(Post.comments))).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    is_liked = False
    if userId:
        like = session.exec(select(UserPostLike).where(UserPostLike.userId == userId, UserPostLike.postId == post_id)).first()
        if like:
            is_liked = True
            
    post_read = PostRead.from_orm(post)
    post_read.isLiked = is_liked
    return post_read

@app.post("/posts/{post_id}/comments", response_model=Comment)
def create_comment(post_id: str, comment: CommentCreate, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user = session.get(User, comment.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    new_comment = Comment(
        id=str(uuid.uuid4()),
        userId=user.id,
        userName=user.name,
        userAvatar=user.avatar,
        content=comment.content,
        post_id=post_id
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@app.post("/posts/{post_id}/like", response_model=PostRead)
def like_post(post_id: str, userId: str = None, session: Session = Depends(get_session)):
    if not userId:
        raise HTTPException(status_code=400, detail="userId is required")
        
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    # Check if already liked
    existing_like = session.exec(select(UserPostLike).where(UserPostLike.userId == userId, UserPostLike.postId == post_id)).first()
    
    if existing_like:
        # Unlike
        session.delete(existing_like)
        post.likes = max(0, post.likes - 1)
        is_liked = False
    else:
        # Like
        new_like = UserPostLike(userId=userId, postId=post_id)
        session.add(new_like)
        post.likes += 1
        is_liked = True
        
    session.add(post)
    session.commit()
    session.refresh(post)
    
    post_read = PostRead.from_orm(post)
    post_read.isLiked = is_liked
    return post_read

@app.post("/events", response_model=EventRead)
def create_event(event: EventCreate, session: Session = Depends(get_session)):
    organizer = session.get(User, event.organizerId)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    new_event = Event(
        id=str(uuid.uuid4()),
        title=event.title,
        description=event.description,
        image=event.image,
        date=event.date,
        time=event.time,
        locationName=event.locationName,
        locationAddress=event.locationAddress,
        lat=event.lat,
        lng=event.lng,
        organizerId=event.organizerId,
        organizerName=organizer.name,
        organizerAvatar=organizer.avatar,
        category=event.category,
        attendeeCount=1,
        isJoined=True,
        isPast=False
    )
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event

@app.get("/events/{event_id}", response_model=EventRead)
def read_event(event_id: str, session: Session = Depends(get_session)):
    event = session.exec(select(Event).where(Event.id == event_id).options(selectinload(Event.ageGroups))).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/events/{event_id}/join", response_model=EventRead)
def join_event(event_id: str, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Toggle join status
    if event.isJoined:
        event.isJoined = False
        event.attendeeCount = max(0, event.attendeeCount - 1)
    else:
        event.isJoined = True
        event.attendeeCount += 1
        
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@app.put("/profile", response_model=User)
def update_profile(user_update: UserUpdate, session: Session = Depends(get_session)):
    # Updating the default user "user-1"
    user = session.get(User, "user-1")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.avatar is not None:
        user.avatar = user_update.avatar
    if user_update.neighborhood is not None:
        user.neighborhood = user_update.neighborhood
    if user_update.bio is not None:
        user.bio = user_update.bio
        
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
