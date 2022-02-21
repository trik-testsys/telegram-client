from flask import request, Request, jsonify

from api.loader import app
from bot.repository.UserRepository import UserRepository


@app.route('/user', methods=['GET', 'POST'])
async def user_handler():
    match request.method:

        case 'GET':
            return await handle_get()

        case 'POST':
            return await handle_post()


async def handle_get() -> (any, int):
    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify(
            code=400,
            message="request must contain user_id arg"
        ).json, 400

    try:
        user = await UserRepository.get_user(user_id)

        if user is None:
            return jsonify(exist=False), 200
        else:
            return jsonify(exist=True), 200

    except Exception:
        return jsonify(
            code=500,
            message="Unexpected error"
        ).json, 500


async def handle_post() -> (any, int):
    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify(
            code=400,
            message="request must contain user_id arg"
        ).json, 400

    user = await UserRepository.get_user(user_id)

    if user is not None:
        return '', 409

    try:
        await UserRepository.create_user(user_id=user_id, role="student")
        return '', 201
    except Exception:
        return jsonify(
            code=500,
            message="Unexpected error"
        ).json, 500
