"""Post management routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.db.models import Post, User
from app.posts.schemas import PostCreate, PostRead, PostUpdate
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=list[PostRead])
def list_posts(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """
    List all posts (public endpoint).
    
    - **skip**: Number of posts to skip (pagination)
    - **limit**: Maximum number of posts to return
    """
    statement = select(Post).offset(skip).limit(limit)
    posts = session.exec(statement).all()
    return posts


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new post (authenticated users only).
    """
    post = Post(
        **post_data.model_dump(),
        author_id=current_user.id
    )
    
    session.add(post)
    session.commit()
    session.refresh(post)
    
    return post


@router.get("/{post_id}", response_model=PostRead)
def get_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    """Get post by ID (public endpoint)."""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@router.put("/{post_id}", response_model=PostRead)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a post.
    
    Users can only update their own posts.
    Admins can update any post.
    """
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check ownership or admin
    if post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )
    
    # Update only provided fields
    update_data = post_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    
    session.add(post)
    session.commit()
    session.refresh(post)
    
    return post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a post.
    
    Users can only delete their own posts.
    Admins can delete any post.
    """
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Check ownership or admin
    if post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    
    session.delete(post)
    session.commit()
    
    return {"message": "Post deleted successfully"}
