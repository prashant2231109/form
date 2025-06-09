from django.db import models
from django.contrib.auth.models import User ,AbstractUser
from .choices import QUESTION_CHOICES
from .utils.utility import generate_random_string

class User(AbstractUser):
    email=models.EmailField(unique=True)


class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract=True      #isse kya hoga database me iska model nhe banega base class treat hoga meta ke andr abstact pass krne se
        

class Choices(BaseModel):
    choice=models.CharField(max_length=100)
    
    def __str__(self):
        return self.choice
    
    class Meta:
        db_table="choice"  #ye kya karega jo choices ke table ke name hoga default me uske jagah ye kr dega
        ordering=['-created_at']

class Questions(BaseModel):
    question_text=models.CharField(max_length=100)
    questions_type=models.CharField(choices=QUESTION_CHOICES,max_length=100)
    required=models.BooleanField(default=False)
    choices=models.ManyToManyField(Choices,related_name="question_choices",blank=True)
    
    
    
    def __str__(self):
        return self.question_text

class Form(BaseModel):
    code=models.CharField(max_length=100 ,unique=True)
    title =models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    creator=models.ForeignKey(User,on_delete=models.CASCADE)    
    background_color=models.CharField(max_length=100,default="#272124")
    collect_email=models.BooleanField(default=False)
    questions=models.ManyToManyField(Questions,related_name="questions")
    
    @staticmethod
    def create_blank_form(user):
        form_token =generate_random_string()
        choices=Choices.objects.create(choice="option 1")
        question =Questions.objects.create(questions_type='multiple choice ',question_text="Untitled question")
        question.choices.add(choices)
        form=Form(code=form_token,title="Untitled form",creator=user)
        form.save()
        form.questions.add(question)
        return form
    
    def __str__(self):
        return self.title
    
class Answers(BaseModel):
    answer=models.CharField(max_length=100)
    answer_to=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name="answer_to")    
    
    def __str__(self):
        return self.answer
    
class Responses(BaseModel):
    response_code=models.CharField(max_length=100,unique=True)
    response_to=models.ForeignKey(Form,on_delete=models.CASCADE)  
    responder_ip=models.CharField(max_length=100)
    responder_email=models.EmailField(null=True,blank=True)
    response=models.ManyToManyField(Answers,related_name="annwer")
    
    def __str__(self):
        return self.response_code
    
