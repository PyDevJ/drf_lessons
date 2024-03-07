import re
from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:
    def __init__(self, field='video_link', message='Ссылка дожна быть только на видео в YouTube'):
        self.field = field
        self.message = message

    def __call__(self, value):
        video_link = value.get(self.field)
        if not video_link:
            return  # Если поле 'video_link' пустое, валидация пропускается
        youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$')
        if not youtube_pattern.match(video_link):
            raise ValidationError({self.field: [self.message]})
