import json, ast, urllib, ssl, random, time, sched, datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from channels import Group,Channel
from channels.auth import channel_session_user, channel_session_user_from_http, channel_session
from example.models import Person, Membership, Game, Question


User = get_user_model()
context = ssl._create_unverified_context()
rooms = {
    "Alfa":{"state":False,"isInitialize": False,"userList":[]},
    "Bravo":{"state":False,"isInitialize": False,"userList":[]}, 
    "Charlie":{"state":False,"isInitialize": False,"userList":[]}, 
    "Delta":{"state":False,"isInitialize": False,"userList":[]}, 
    "Echo":{"state":False,"isInitialize": False,"userList":[]}, 
    "Foxtrot":{"state":False,"isInitialize": False,"userList":[]}, 
    "Golf":{"state":False,"isInitialize": False,"userList":[]}, 
    "Hotel":{"state":False,"isInitialize": False,"userList":[]}, 
    "India":{"state":False,"isInitialize": False,"userList":[]},
    "Juliett":{"state":False,"isInitialize": False,"userList":[]}
}
users = {}
backgroundActivated = False
# controlTwice = False

@channel_session
def ws_connect(message,room_name):

    # if backgroundActivated is False:
    #     Channel('background').send({})
    questionsCount = Question.objects.all().count()
    if questionsCount<120:
        for i in range(120-questionsCount):
            Question(question="",correct_answer="",wrong_answer_one = "", wrong_answer_two = "", wrong_answer_three="").save()
    connectable = rooms[room_name]["state"] == False
    if connectable is False:
        for (tag,room) in rooms.items():
            if room['state'] is False:
                message.reply_channel.send({
                    "close":True,
                    "text":json.dumps({
                        'info': "loginAttempt",
                        'connected': False,
                        'findRoom': True,
                        'roomName': tag
                    })
                })
                break
            elif tag == "Juliett":
                 message.reply_channel.send({
                    "close":True,
                    "text":json.dumps({
                        'info': "loginAttempt",
                        'connected': False,
                        'findRoom': False
                    })
                })
    else:
        availables = Person.objects.filter(~Q(name__in=users.keys()))
        selectedPerson = random.choice(availables)
        users[selectedPerson.name] = message.reply_channel
        rooms[room_name]["userList"].append(selectedPerson.name)
        Group(room_name).send({
            "text":json.dumps({
                "info": "updateUserList",
                "message": selectedPerson.name + "is connected now",
                "user_list": rooms[room_name]["userList"]
            })
        })
        Group(room_name).add(message.reply_channel)
        message.reply_channel.send({
            "text":json.dumps({
                'info': "loginAttempt",
                'connected': True,
                'name': selectedPerson.name,
                'wild_card': selectedPerson.wild_card
            })
        })


@channel_session
def ws_message(message,room_name):
    # print(message.content["text"])
    myDict = json.loads(message.content['text'])
    
    info = myDict["info"]
    if info == "initialPerson":
        if rooms[room_name]["isInitialize"] is False:
            selectedPeople = Person.objects.filter(~Q(name__in=users.keys())).order_by('?')[0:5]
            for person in selectedPeople:
                users[person.name] = None
                rooms[room_name]["userList"].append(person.name)
            message.reply_channel.send({
                "text":json.dumps({
                    "info": "initialPerson",
                    "status": True

                })
            })
            Group(room_name).send({
                "text":json.dumps({
                    "info": "updateUserList",
                    "message": "5 Person Added",
                    "user_list": rooms[room_name]["userList"]
                })
            })
            responseDict = json.loads(urllib.request.urlopen(urllib.request.Request('https://opentdb.com/api.php?amount=12&type=multiple'),context=context).read())
            Group(room_name).send({
                "text":json.dumps({
                    "info": "startGame",
                    "questions": responseDict["results"]
                })
            })
            rooms[room_name]["isInitialize"] = True
            rooms[room_name]["state"] = True
        else:
            message.reply_channel.send({
                "text":json.dumps({
                    "info": "initialPerson",
                    "status": False
                })
            })
    # elif info == "getQuestions":
    #     Group(room_name).send({
    #         'text': "Canimsin"
    #     })
    # if myDict["action"] == "login":
    #     Group('users').send({
    #         'text': json.dumps({
    #             "text": "Good"
    #         })
    #     })
    # elif myDict["action"] == "getQuestions":
    #     Group('users').send({
    #         'text': urllib.request.urlopen(urllib.request.Request('https://opentdb.com/api.php?amount=10'),context=context).read().decode('utf-8',"replace")
    #     })
    # message.reply_channel.send({"text": "Adamsin"})

@channel_session
def ws_disconnect(message,room_name):

    isInRoom = False
    named = ""
    for (username,channel) in users.items():
        if channel != None and channel.name == message.reply_channel.name and (username in rooms[room_name]["userList"]):
            isInRoom = True
            named = username
            break
    if isInRoom:
        Group(room_name).discard(message.reply_channel)
        if named in rooms[room_name]["userList"]: rooms[room_name]["userList"].remove(named)
        if rooms[room_name]["state"] is True:
            # Membership.objects.filter(is_active=True)
            pass
        else:
            Group(room_name).send({
                "text":json.dumps({
                    "info": "updateUserList",
                    "message": named + " is disconnected now",
                    "user_list": rooms[room_name]["userList"]
                })
            })

def background_task(message):
    s = sched.scheduler(time.time, time.sleep)
    # global controlTwice
    def task_definiton(sc):
        # roomNames = ["Alfa","Bravo","Charlie","Delta","Echo","Foxtrot","Golf","Hotel","India","Juliett"]
        # controlGames = Game.objects.filter(is_active=True)
        # for checkedGame in controlGames:
        #     secondPassed = int((timezone.now() - checkedGame.timestamp).total_seconds())
        #     if secondPassed < 65:
        #         pass
        #     elif secondPassed < 125:
        #         if checkedGame.currentQuestion == 1:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 2
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             })
        #     elif secondPassed < 185:
        #         if checkedGame.currentQuestion == 2:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 3
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 245:
        #         if checkedGame.currentQuestion == 3:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 4
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 305:
        #         if checkedGame.currentQuestion == 4:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 5
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 365:
        #         if checkedGame.currentQuestion == 5:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 6
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 425:
        #         if checkedGame.currentQuestion == 6:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 7
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 485:
        #         if checkedGame.currentQuestion == 7:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 8
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 545:
        #         if checkedGame.currentQuestion == 8:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 9
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 605:
        #         if checkedGame.currentQuestion == 9:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 10
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             }) 
        #     elif secondPassed < 665:
        #         if checkedGame.currentQuestion == 10:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 11
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             })
        #     elif secondPassed < 725:
        #         if checkedGame.currentQuestion == 11:
        #             roomOrder = roomNames.index(checkedGame.room)
        #             checkedGame.currentQuestion = 12
        #             checkedGame.save()
        #             question = Question.objects.get(pk=checkedGame.currentQuestion+(roomOrder*12))
        #             answers = [question.correct_answer,question.wrong_answer_one,question.wrong_answer_two,question.wrong_answer_three]
        #             random.shuffle(answers)
        #             Group(checkedGame.room).send({
        #                 "text":json.dumps({
        #                     "info": "newQuestion",
        #                     "question": question.question,
        #                     "answers": answers
        #                 })
        #             })
        #     elif secondPassed < 785:
        #         if checkedGame.currentQuestion == 12:
        #             rooms[checkedGame.room]["state"] = False
        #             rooms[checkedGame.room]["isInitialize"] = False
        #             Membership.objects.filter(person__name__in=rooms[checkedGame.room]["userList"],game=checkedGame,isFailed=False)
        #             checkedGame.is_active=False
        #             checkedGame.save()
        #     else:
        #         pass
        # # if controlTwice:
        # for (tag,room) in rooms.items():
        #     if room["isInitialize"] == True and room["state"] is False:
        #         roomOrder = roomNames.index(tag)
        #         index = 0
        #         questions = Question.objects.filter(pk__in=range(1+(roomOrder*12),13+(roomOrder*12)))
        #         responseDict = json.loads(urllib.request.urlopen(urllib.request.Request('https://opentdb.com/api.php?amount=12&type=multiple'),context=context).read())
        #         for question in questions:
        #             question.question = responseDict["results"][index]["question"]
        #             question.correct_answer = responseDict["results"][index]["correct_answer"]
        #             question.wrong_answer_one = responseDict["results"][index]["incorrect_answers"][0]
        #             question.wrong_answer_two = responseDict["results"][index]["incorrect_answers"][1]
        #             question.wrong_answer_three = responseDict["results"][index]["incorrect_answers"][2]
        #             question.save()
        #             index = index + 1
        #         persons = Person.objects.filter(name__in = room["userList"])
        #         game = Game(is_active=True,room=tag,currentQuestion=1)
        #         game.save()
        #         for person in persons:
        #             Membership(person=person,game=game).save()
        #         room["state"] = True
        #         answers = [questions[0].correct_answer,questions[0].wrong_answer_one,questions[0].wrong_answer_two,questions[0].wrong_answer_three]
        #         random.shuffle(answers)
        #         Group(tag).send({
        #             "text":json.dumps({
        #                 "info": "starting",
        #                 "question": questions[0].question,
        #                 "answers": answers
        #             })
        #         })
        s.enter(5,30,task_definiton, (sc,))
    s.enter(5,30,task_definiton, (s,))
    s.run()



