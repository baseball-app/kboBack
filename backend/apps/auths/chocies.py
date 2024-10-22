from enum import Enum


class SocialTypeEnum(Enum):
    NONE = 0
    NAVER = 1
    KAKAO = 2

    @classmethod
    def full_choices(cls):
        return [(social_type.value, social_type.name) for social_type in cls]
