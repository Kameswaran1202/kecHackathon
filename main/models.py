from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager

# Create your models here.


class Article(models.Model):
    visibilityChoice = (
        ('public','public'),
        ('private','private'),
        ('deleted','deleted')
    )
    statusChoice = (
        ('draft', 'draft'),
        ('published', 'published')
    )
    slug = models.CharField(max_length=35, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=statusChoice, max_length=60, default='draft', null=True, blank=True)
    visibility = models.CharField(choices=visibilityChoice, max_length=70, default='public', null=True, blank=True)
    dt_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dt_updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dt_published = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    highlight = models.BooleanField(default=False, null=True, blank=True)
    iskecian = models.BooleanField(default=False, blank=True, null=True)
    isofficial = models.BooleanField(default=False, blank=True, null=True)
    forfirst = models.BooleanField(default=False, blank=True, null=True)
    forsecond = models.BooleanField(default=False, blank=True, null=True)
    forthird = models.BooleanField(default=False, blank=True, null=True)
    forfinal = models.BooleanField(default=False, blank=True, null=True)
    isspl = models.BooleanField(default=False, blank=True, null=True)
    tags = TaggableManager(blank=True)
    
    # likes = models.ManyToManyField(User, blank=True)
    # reports = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return f'{self.title}'


class ArticleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    dt_liked = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}-{self.article.title}'



class ArticleReport(models.Model):
    reason_choice = (
        ('Sexual content', 'Sexual content'),
        ('Violent or repulsive content', 'Violent or repulsive content'),
        ('Hateful or abusive content', 'Hateful or abusive content'),
        ('Harassment or bullying', 'Harassment or bullying'),
        ('Harmful or dangerous acts', 'Harmful or dangerous acts'),
        ('Misinformation', 'Misinformation'),
        ('Child abuse', 'Child abuse'),
        ('Promotes terrorism', 'Promotes terrorism'),
        ('Spam or misleading', 'Spam or misleading'),
        ('Infringes my rights', 'Infringes my rights'),
        ('Captions issue', 'Captions issue'),
    )
    reason = models.CharField(choices=reason_choice, max_length=70, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    dt_reported = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    def __str__(self):
        return f'{self.user.username}-{self.article.title}'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.follower.username} - {self.followed.username}'
    
class Comment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    cmt_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    # def __str__(self):
    #     return self.comment[0:13] + "..."+ "by" + self.user.username