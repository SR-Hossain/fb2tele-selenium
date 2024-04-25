from bot.fetch.ai import test_ai_response
from bot.fetch.browser import Browser
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from bot.fetch.fb2tele import FB2Tele
from bot.fetch.tele_bot import test_telebot
from bot.serializers import ActionSerializer, Action
from fb2tele.settings import env


class BotStatusAPIView(GenericAPIView):
    serializer_class = ActionSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.validated_data['action']
            if action == Action.CHECK_STATUS:
                browser = Browser()

                facebook_response_data = browser.get_html_data(
                    url=f"https://mbasic.facebook.com/groups/{env.str('FACEBOOK_GROUP_ID')}/")

                return Response({
                    'facebook status code': facebook_response_data,
                    'ai status code': test_ai_response(),
                    'telegram status code': test_telebot()
                })

            elif action == 'fetch_posts':
                try:
                    fb2tele = FB2Tele()
                    if fb2tele.get_new_post_permalinks():
                        fb2tele.start()
                        return Response({'status': 'Telegram bot has started fetching.'})
                    else:
                        return Response({'status': 'No new posts found.'})
                except Exception as e:
                    return Response({'status': f'Failed to fetch posts. Error: {e}'})
            return Response({'status': 'Action completed successfully.'})
        else:
            return Response(serializer.errors, status=400)

