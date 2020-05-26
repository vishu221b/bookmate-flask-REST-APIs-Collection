from flask_restful import Resource
from service import UserSocialService
from flask_jwt_extended import jwt_required, get_jwt_identity


class FollowUnfollowUsers(Resource):
    @jwt_required
    def post(self, action, user_to_be_followed_unfollowed):
        user_social_service = UserSocialService()
        performer = get_jwt_identity()
        response = user_social_service.follow_unfollow_a_user(
            performer.get('email'), user_to_be_followed_unfollowed, action.upper()
        )
        return response[0], response[1]
