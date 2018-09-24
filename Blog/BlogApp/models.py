from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BlogModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,default = 1)
    text = models.CharField(max_length=255)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.text

    def user_can_vote(self,user):
        '''
        Return False if the user already voted else True.
        '''
        user_vote = user.vote_set.all()
        qs = user_vote.filter(blog=self)
        if qs.exists():
            return False
        return True

    @property
    def num_votes(self):
        return self.vote_set.count()

    def get_result_dict(self):
        '''
        Return a list of objects in the form:
        [
            # for each related choice:
            {
                'text' : choice_text,
                'num_votes' num_votes of votes on that choice,
                'percentage': num_votes / poll.num_votes * 100
            }
        ]
        '''
        
        res = []
        for choice in self.choice_set.all():
            d = {}
            d['text'] = choice.choice_text
            d['num_votes'] = choice.num_votes
            if not self.num_votes:
                d['percentage'] = 0
            else:
                d['percentage'] = choice.num_votes / self.num_votes * 100
            res.append(d)
        return res

class Choice(models.Model):
    blog = models.ForeignKey(BlogModel,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.blog.text[:25],self.choice_text[:25])

    @property
    def num_votes(self):
        return self.vote_set.count()

class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogModel,on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
