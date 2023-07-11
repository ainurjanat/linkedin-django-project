from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = {User.first_name} + {User.last_name}
    headline = models.CharField(max_length=200)
    bio = models.TextField()

    def __str__(self):
        return self.full_name
    
class Connection(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_connections')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    # user.liked_posts.all() for all liked posts

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"