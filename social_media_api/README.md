# Social Media API

A Django REST API that provides social media functionality including user management, posts, comments, user following, personalized feeds, **post likes**, and **real-time notifications**.

## Features

- **User Management**: Registration, login, and profile management
- **Posts & Comments**: Create, read, update, and delete posts and comments
- **User Following**: Follow/unfollow other users
- **Personalized Feed**: View posts from users you follow
- **Post Likes**: Like and unlike posts with duplicate prevention
- **Real-time Notifications**: Get notified about likes, follows, and comments
- **Token Authentication**: Secure API access using Django REST Framework tokens

## Project Structure

```
social_media_api/
├── accounts/           # User management app
│   ├── models.py      # CustomUser model with following functionality
│   ├── views.py       # User views (register, login, follow, etc.)
│   ├── serializers.py # User data serialization
│   └── urls.py        # User-related URL patterns
├── posts/             # Posts, comments, and likes app
│   ├── models.py      # Post, Comment, and Like models
│   ├── views.py       # Post views, feed, and like functionality
│   ├── serializers.py # Post/Comment/Like data serialization
│   └── urls.py        # Post-related URL patterns
├── notifications/     # Notification system app
│   ├── models.py      # Notification model with GenericForeignKey
│   ├── views.py       # Notification management views
│   ├── serializers.py # Notification data serialization
│   └── urls.py        # Notification-related URL patterns
└── social_media_api/  # Main project settings
    ├── settings.py    # Django configuration
    └── urls.py        # Main URL routing
```

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication

All endpoints except registration and login require authentication using a token in the Authorization header:

```
Authorization: Token <your-token-here>
```

### User Management

#### Register User

- **URL**: `POST /api/register/`
- **Description**: Create a new user account
- **Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword",
    "password2": "securepassword",
    "bio": "Hello, I'm John!"
  }
  ```

#### Login User

- **URL**: `POST /api/login/`
- **Description**: Authenticate user and receive token
- **Body**:
  ```json
  {
    "username": "johndoe",
    "password": "securepassword"
  }
  ```
- **Response**: Returns user data and authentication token

#### Get User Profile

- **URL**: `GET /api/profile/`
- **Description**: Get current user's profile information
- **Authentication**: Required

#### Follow User

- **URL**: `POST /api/follow/<user_id>/`
- **Description**: Follow another user
- **Body**:
  ```json
  {
    "user_id": 2
  }
  ```
- **Authentication**: Required
- **Notifications**: Creates notification for the followed user

#### Unfollow User

- **URL**: `POST /api/unfollow/<user_id>/`
- **Description**: Unfollow another user
- **Body**:
  ```json
  {
    "user_id": 2
  }
  ```
- **Authentication**: Required

### Posts & Comments

#### Create Post

- **URL**: `POST /api/posts/`
- **Description**: Create a new post
- **Body**:
  ```json
  {
    "title": "My First Post",
    "content": "This is the content of my first post!"
  }
  ```
- **Authentication**: Required

#### Get All Posts

- **URL**: `GET /api/posts/`
- **Description**: Retrieve all posts (read-only for non-authenticated users)
- **Response**: Includes `likes_count` and `is_liked` fields

#### Get Single Post

- **URL**: `GET /api/posts/<post_id>/`
- **Description**: Retrieve a specific post

#### Update Post

- **URL**: `PUT /api/posts/<post_id>/`
- **Description**: Update a post (only by author)
- **Authentication**: Required

#### Delete Post

- **URL**: `DELETE /api/posts/<post_id>/`
- **Description**: Delete a post (only by author)
- **Authentication**: Required

#### Create Comment

- **URL**: `POST /api/comments/`
- **Description**: Add a comment to a post
- **Body**:
  ```json
  {
    "content": "Great post!",
    "post": 1
  }
  ```
- **Authentication**: Required
- **Notifications**: Creates notification for the post author

#### Get Comments

- **URL**: `GET /api/comments/`
- **Description**: Retrieve all comments

### **NEW: Post Likes System**

#### Like a Post

- **URL**: `POST /api/posts/<post_id>/like/`
- **Description**: Like a specific post
- **Authentication**: Required
- **Features**: 
  - Prevents duplicate likes
  - Creates notification for post author
  - Returns like details
- **Response**:
  ```json
  {
    "detail": "Post liked successfully",
    "like": {
      "id": 1,
      "user": 2,
      "user_username": "johndoe",
      "created_at": "2025-08-23T18:54:00Z"
    }
  }
  ```

#### Unlike a Post

- **URL**: `POST /api/posts/<post_id>/unlike/`
- **Description**: Remove like from a post
- **Authentication**: Required
- **Response**:
  ```json
  {
    "detail": "Post unliked successfully"
  }
  ```

#### Get Post Likes

- **URL**: `GET /api/posts/<post_id>/likes/`
- **Description**: Get all likes for a specific post
- **Response**:
  ```json
  {
    "post_id": 1,
    "likes_count": 3,
    "likes": [
      {
        "id": 1,
        "user": 2,
        "user_username": "johndoe",
        "created_at": "2025-08-23T18:54:00Z"
      }
    ]
  }
  ```

### **NEW: Notification System**

#### Get User Notifications

- **URL**: `GET /api/notifications/`
- **Description**: Get all notifications for the current user
- **Authentication**: Required
- **Query Parameters**:
  - `unread=true` - Show only unread notifications
  - `type=like` - Filter by notification type
- **Response**:
  ```json
  {
    "notifications": [
      {
        "id": 1,
        "recipient": 1,
        "recipient_username": "alice",
        "actor": 2,
        "actor_username": "bob",
        "verb": "liked your post",
        "notification_type": "like",
        "target_info": {
          "type": "post",
          "title": "My First Post"
        },
        "timestamp": "2025-08-23T18:54:00Z",
        "is_read": false
      }
    ],
    "total_count": 5,
    "unread_count": 3,
    "message": "Found 5 notifications"
  }
  ```

#### Mark Notification as Read

- **URL**: `POST /api/notifications/<notification_id>/mark-read/`
- **Description**: Mark a specific notification as read
- **Authentication**: Required

#### Mark All Notifications as Read

- **URL**: `POST /api/notifications/mark-all-read/`
- **Description**: Mark all notifications as read
- **Authentication**: Required

#### Delete Notification

- **URL**: `DELETE /api/notifications/<notification_id>/delete/`
- **Description**: Delete a specific notification
- **Authentication**: Required

#### Get Notification Statistics

- **URL**: `GET /api/notifications/stats/`
- **Description**: Get notification statistics for the current user
- **Authentication**: Required
- **Response**:
  ```json
  {
    "total_count": 10,
    "unread_count": 4,
    "type_counts": {
      "follow": 2,
      "like": 5,
      "comment": 3,
      "mention": 0
    }
  }
  ```

### Feed Functionality

#### Get User Feed

- **URL**: `GET /api/feed/`
- **Description**: Get posts from users that the current user follows
- **Authentication**: Required
- **Response**: Returns posts ordered by creation date (newest first)
- **Features**: Now includes like counts and like status for each post

## Data Models

### CustomUser

- Extends Django's AbstractUser
- Additional fields: `bio`, `profile_picture`, `following`
- Methods: `follow()`, `unfollow()`, `is_following()`
- Properties: `followers_count`, `following_count`

### Post

- Fields: `author`, `title`, `content`, `created_at`, `updated_at`
- Related to CustomUser through ForeignKey
- **NEW**: Related to Like through ForeignKey with `related_name='likes'`

### Comment

- Fields: `post`, `author`, `content`, `created_at`, `updated_at`
- Related to Post and CustomUser through ForeignKey

### **NEW: Like**

- Fields: `post`, `user`, `created_at`
- Related to Post and CustomUser through ForeignKey
- **Features**:
  - Unique constraint prevents duplicate likes
  - Ordered by creation date (newest first)
  - Related names: `post.likes`, `user.user_likes`

### **NEW: Notification**

- Fields: `recipient`, `actor`, `verb`, `notification_type`, `content_type`, `object_id`, `target`, `timestamp`, `is_read`
- **Features**:
  - GenericForeignKey for flexible target objects
  - Notification types: follow, like, comment, mention
  - Read/unread status tracking
  - Indexed for performance
  - Ordered by timestamp (newest first)

## Testing the API

### Quick Test

1. **Start the server**
   ```bash
   python manage.py runserver
   ```

2. **Run the comprehensive test script**
   ```bash
   python test_likes_notifications.py
   ```

### Manual Testing

1. **Register users and create posts**
2. **Test following functionality**
3. **Test liking/unliking posts**
4. **Check notifications for various actions**
5. **Verify personalized feed with like information**

## Example Usage

### Using curl

#### Like a Post
```bash
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json"
```

#### Get Notifications
```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token <your-token>"
```

#### Mark Notification as Read
```bash
curl -X POST http://localhost:8000/api/notifications/1/mark-read/ \
  -H "Authorization: Token <your-token>"
```

### Using Python requests

```python
import requests

# Like a post
response = requests.post(
    'http://localhost:8000/api/posts/1/like/',
    headers={'Authorization': f'Token {token}'}
)

# Get notifications
response = requests.get(
    'http://localhost:8000/api/notifications/',
    headers={'Authorization': f'Token {token}'}
)

# Get unread notifications only
response = requests.get(
    'http://localhost:8000/api/notifications/?unread=true',
    headers={'Authorization': f'Token {token}'}
)
```

## Notification Triggers

The system automatically creates notifications for:

1. **Follows**: When user A follows user B
2. **Likes**: When user A likes user B's post
3. **Comments**: When user A comments on user B's post

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data (e.g., duplicate like)
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Security Features

- Token-based authentication
- Password validation
- User permission checks
- CSRF protection
- Input validation and sanitization
- **NEW**: Duplicate like prevention
- **NEW**: User-specific notification access

## Performance Features

- **NEW**: Database indexes on notification fields
- **NEW**: Efficient like queries with related names
- **NEW**: Optimized notification filtering and counting

## Future Enhancements

- Pagination for posts, comments, and notifications
- Search functionality
- Image upload support
- Real-time notifications (WebSocket)
- User blocking functionality
- Post categories and tags
- **NEW**: Notification preferences and settings
- **NEW**: Bulk notification operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
