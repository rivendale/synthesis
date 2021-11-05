import graphene
from django.conf import settings
from django.db.models.expressions import F
from graphql_extensions.auth.decorators import login_required

from ..helpers.constants import SUCCESS_MESSAGE
from ..helpers.email import send_mail_
from ..helpers.permissions import check_token_iat, token_required
from ..helpers.validate_input import check_missing_fields
from ..helpers.validate_object_id import validate_object_id
from .models import Choice, Feedback, Question, UserFeedback
from .object_types import ChoiceInput, FeedbackInput, UserFeedbackInput


class FeedbackChoice(graphene.Mutation):
    '''Handle submit feedback'''
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the submittion of feedback'''
        input = ChoiceInput(required=True)

    @token_required
    @check_token_iat
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for submittion of feedback. Actual saving happens here'''
        input = kwargs.get("input", {})
        choice_ids = input.get("choice_ids", [])
        valid_choice_ids = []
        for id_ in choice_ids:
            choice = validate_object_id(id_, Choice, "Choice")
            valid_choice_ids.append(choice)
        for choice in valid_choice_ids:
            choice.votes = F("votes") + 1
            choice.save(update_fields=["votes"])
        status = "Success"

        return FeedbackChoice(status=status,
                              message=SUCCESS_MESSAGE.format("Feedback Submitted"))


class QuestionFeedback(graphene.Mutation):
    '''Handle submit feedback'''
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the submittion of feedback'''
        input = FeedbackInput(required=True)

    @token_required
    @check_token_iat
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for submittion of feedback. Actual saving happens here'''
        input = kwargs.get("input", {})
        check_missing_fields(input, ['feedback'])
        feedback_input = input.get("feedback", [])

        for feedback_question in feedback_input:
            question_id = feedback_question.get("question_id", "")
            feedback_text = feedback_question.get("feedback_text", "")
            if feedback_text:
                feedback = Feedback(**{"feedback_text": feedback_text})

            if question_id:
                question = validate_object_id(question_id, Question, "Question")
                feedback.question = question

            feedback.save()
        status = "Success"

        return FeedbackChoice(status=status,
                              message=SUCCESS_MESSAGE.format("Feedback Submitted"))


class SendUserFeedback(graphene.Mutation):
    '''Handle submit feedback'''
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the submittion of feedback'''
        input = UserFeedbackInput(required=True)

    @token_required
    @check_token_iat
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for submittion of feedback. Actual saving happens here'''
        input = kwargs.get("input", {})
        check_missing_fields(input, ['feedback', 'feedback_page'])
        feedback_input = input.get("feedback", "")
        feedback_page = input.get("feedback_page", "")
        feedback = UserFeedback(
            **{"feedback": feedback_input,
               'feedback_page': feedback_page,
               "user": info.context.user})
        feedback.save()
        status = "Success"
        username = feedback.user.username
        email = feedback.user.email
        html_content = \
            f'<p><b>{username}-[{email}] says:</b> <br/>{feedback.feedback}</p>'

        subject = f'You have received feedback from {username}-[{feedback.user.email}]'
        send_mail_.delay(
            subject=subject,
            message=subject,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[settings.FEEDBACK_EMAIL],
            html_message=html_content,
            fail_silently=False,)

        return SendUserFeedback(status=status,
                                message=SUCCESS_MESSAGE.format("Feedback Submitted"))


class Mutation(graphene.ObjectType):
    submit_feedback = FeedbackChoice.Field()
    question_feedback = QuestionFeedback.Field()
    user_feedback = SendUserFeedback.Field()
