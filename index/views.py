from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from index.models import Form,User, Questions,Choices
from .serializers import FormSerializer,QuestionsSerializer,ChoicesSerializer


class FormAPI(APIView):
    
    def get(self,request):
        
        return Response({
            'status':True,
            'message':'Get method called'
        })
    def post(self,request):
        
        try:
            data=request.data
            user=User.objects.first()
            form=Form().create_blank_form(user)
            serializer=FormSerializer(form)
            
        
            return Response({
            'status':True,
            'message':'form created sucessfully',
            'data':serializer.data
            })
        except  Exception as e:
            print(e)
            return Response({
            'status':False,
            'message':'something went wrong',
            'data':{}
            })
    
    
    def patch(self,request):
        try:
            data=request.data
            if  not data.get('form_id'):
                return Response({
                'status':False,
                'message':'form_id is required',
                'data':{}
            })
                
            form_obj=Form.objects.filter(id=data.get('form_id'))
            
            
            if form_obj.exists():
                serializer =FormSerializer(form_obj[0],data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                    'status':True,
                    'message':'form updated is sucessfully',
                    'data':serializer.data
                    })
                
                return Response({
                'status':False,
                'message':'form  not updated ',
                'data':serializer.errors
                })    
            
            
            return Response({
                'status':False,
                'message':'invalid form_id ',
                'data':{}
                })     
        except  Exception as e:
            print(e)
            return Response({
            'status':False,
            'message':'something went wrong',
            'data':{}
            })
            
class QuestionAPI(APIView):       
    
    def post(self,request):
        try:
            
            data=request.data
            data['question_text']='Untitled Question' 
            data['questions_type']='multiple choice'
            
            if  not data.get('form_id'):
                    return Response({
                    'status':False,
                    'message':'form_id is required',
                    'data':{}
                })
            
            serializer = QuestionsSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                form=Form.objects.get(id=data['form_id'])
                form.questions.add(Questions.objects.get(id=serializer.data['id']))
                
                return Response({
                        'status':True,
                        'message':'question created',
                        'data':serializer.data
                })
                
            return Response({
                        'status':False,
                        'message':'question is invalid',
                        'data':serializer.errors
                })
        except  Exception as e:
            print(e)
            return Response({
            'status':False,
            'message':'something went wrong',
            'data':{}
            }) 
            
            
    def patch(self,request):
        try:
            data=request.data
            
            if  not data.get('question_id'):
                        return Response({
                        'status':False,
                        'message':'question_id is required',
                        'data':{}
                    })
            
            question_obj=Questions.objects.get(id=data.get('question_id'))  
            
            
                
            serializer =QuestionsSerializer(question_obj,data=data,partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':True,
                    'message':'question updated ',
                    'data':serializer.data
                    })  
            return Response({
                    'status':False,
                    'message':'qesestion field is not valid ',
                    'data':serializer.errors
                    }) 
            
            
        except Questions.DoesNotExist:
                return Response({
                    'status': False,
                    'message': 'invalid question_id',
                    'data': {}
                })    
        except Exception as e:
            print(e)
            return Response({
            'status':False,
            'message':'something went wrong',
            'data':{}
            })
            
            
            
class ChoiceAPI(APIView):
    def post(self, request):
        data= request.data
        if not data.get('form_id') or not data.get('question_id'):
            return Response({
                        'status':False,
                        'message':' form_id and question_id is required',
                        'data':{}
                    })
        data['choice']='Option'   
        serializer=ChoicesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            form=Form.objects.get(id=data['form_id'])
            form.questions.get(id=data['question_id']).choices.add(Choices.objects.get(id=serializer.data['id']))
            
            return Response({
                        'status':True,
                        'message':' choice created',
                        'data':serializer.data
                    })
        return Response({
                    'status':False,
                    'message':'form  not updated ',
                    'data':serializer.errors
                    })   
    def patch(self , request):
        try:
            data=request.data
            if not data.get('choice_id'):
                return Response({
                            'status':False,
                            'message':' choice_id is required',
                            'data':{}
                        })
                
            choice_obj=Choices.objects.filter(id=data.get('choice_id'))  
            
            
            if  choice_obj.exists():
                    serializer =ChoicesSerializer(choice_obj[0],data=data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                        'status':True,
                        'message':'choice updated is sucessfully',
                        'data':serializer.data
                        })
                
                    return Response({
                    'status':False,
                    'message':'form  not updated ',
                    'data':serializer.errors
                    })    
                
            
            return Response({
                'status':False,
                'message':'invalid choice_id ',
                'data':{}
                })     
        except  Exception as e:
            print(e)
            return Response({
            'status':False,
            'message':'something went wrong',
            'data':{}
            })        

            
    