from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    avatar: str
    neighborhood: str
    bio: str
    joinedDate: str

class UserPostLike(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    userId: str
    postId: str


class Comment(SQLModel, table=True):
    id: str = Field(primary_key=True)
    userId: str
    userName: str
    userAvatar: str
    content: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    post_id: Optional[str] = Field(default=None, foreign_key="post.id")
    post: Optional["Post"] = Relationship(back_populates="comments")

class Post(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    subtitle: str
    content: str
    image: str
    authorId: str
    authorName: str
    authorAvatar: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    likes: int = Field(default=0)
    
    comments: List[Comment] = Relationship(back_populates="post")

class AttendeeAgeGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    range: str
    count: int
    event_id: Optional[str] = Field(default=None, foreign_key="event.id")
    event: Optional["Event"] = Relationship(back_populates="ageGroups")

class Event(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    description: str
    image: str
    date: str
    time: str
    locationName: str
    locationAddress: str
    lat: float
    lng: float
    organizerId: str
    organizerName: str
    organizerAvatar: str
    category: str
    attendeeCount: int = Field(default=0)
    isJoined: bool = Field(default=False)
    isPast: bool = Field(default=False)

    ageGroups: List[AttendeeAgeGroup] = Relationship(back_populates="event")


# Pydantic Schemas for Creation and Updates

class PostCreate(SQLModel):
    title: str
    subtitle: str
    content: str
    image: str
    authorId: str

class CommentCreate(SQLModel):
    userId: str
    content: str

class EventCreate(SQLModel):
    title: str
    description: str
    image: str
    date: str
    time: str
    locationName: str
    locationAddress: str
    lat: float
    lng: float
    organizerId: str
    category: str

class UserUpdate(SQLModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    neighborhood: Optional[str] = None
    bio: Optional[str] = None

# Read Models with Relationships
class PostRead(SQLModel):
    id: str
    title: str
    subtitle: str
    content: str
    image: str
    authorId: str
    authorName: str
    authorAvatar: str
    createdAt: datetime
    likes: int
    isLiked: bool = False
    comments: List[Comment] = []


class EventRead(SQLModel):
    id: str
    title: str
    description: str
    image: str
    date: str
    time: str
    locationName: str
    locationAddress: str
    lat: float
    lng: float
    organizerId: str
    organizerName: str
    organizerAvatar: str
    category: str
    attendeeCount: int
    isJoined: bool
    isPast: bool
    ageGroups: List[AttendeeAgeGroup] = []
