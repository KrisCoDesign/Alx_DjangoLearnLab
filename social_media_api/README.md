# Social Media API

A Django REST API that provides social media functionality including user management, posts, comments, user following, and personalized feeds.

## Features

- **User Management**: Registration, login, and profile management
- **Posts & Comments**: Create, read, update, and delete posts and comments
- **User Following**: Follow/unfollow other users
- **Personalized Feed**: View posts from users you follow
- **Token Authentication**: Secure API access using Django REST Framework tokens

## Project Structure

```
social_media_api/
├── accounts/           # User management app
│   ├── models.py      # CustomUser model with following functionality
│   ├── views.py       # User views (register, login, follow, etc.)
│   ├── serializers.py # User data serialization
│   └── urls.py        # User-related URL patterns
├── posts/             # Posts and comments app
│   ├── models.py      # Post and Comment models
│   ├── views.py       # Post views and feed functionality
│   ├── serializers.py # Post/Comment data serialization
│   └── urls.py        # Post-related URL patterns
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

#### Get Comments

- **URL**: `GET /api/comments/`
- **Description**: Retrieve all comments

### Feed Functionality

#### Get User Feed

- **URL**: `GET /api/feed/`
- **Description**: Get posts from users that the current user follows
- **Authentication**: Required
- **Response**: Returns posts ordered by creation date (newest first)

## Data Models

### CustomUser

- Extends Django's AbstractUser
- Additional fields: `bio`, `profile_picture`, `following`
- Methods: `follow()`, `unfollow()`, `is_following()`
- Properties: `followers_count`, `following_count`

### Post

- Fields: `author`, `title`, `content`, `created_at`, `updated_at`
- Related to CustomUser through ForeignKey

### Comment

- Fields: `post`, `author`, `content`, `created_at`, `updated_at`
- Related to Post and CustomUser through ForeignKey

## Testing the API

1. **Start the server**

   ```bash
   python manage.py runserver
   ```

2. **Run the test script**
   ```bash
   python test_api.py
   ```

The test script will:

- Register two test users
- Create posts for both users
- Test the follow functionality
- Verify the feed shows posts from followed users

## Example Usage

### Using curl

1. **Register a user**

   ```bash
   curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password2":"testpass123"}'
   ```

2. **Login and get token**

   ```bash
   curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"testpass123"}'
   ```

3. **Create a post (using token from login)**

   ```bash
   curl -X POST http://localhost:8000/api/posts/ \
     -H "Authorization: Token <your-token>" \
     -H "Content-Type: application/json" \
     -d '{"title":"My Post","content":"Post content here"}'
   ```

4. **Get your feed**
   ```bash
   curl -X GET http://localhost:8000/api/feed/ \
     -H "Authorization: Token <your-token>"
   ```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
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

## Future Enhancements

- Pagination for posts and comments
- Search functionality
- Image upload support
- Real-time notifications
- User blocking functionality
- Post categories and tags

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
