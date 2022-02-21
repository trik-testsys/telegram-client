from flask import jsonify, request

from api.loader import app
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.UserRepository import UserRepository


@app.route('/submit', methods=['GET'])
async def handler():
    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify(
            code=400,
            message="request must contain user_id arg"
        ).json, 400

    user = await UserRepository.get_user(user_id)

    if user is None:
        return jsonify(
            code=400,
            message=f"user with user_id={user_id} not exist"
        ), 400

    try:
        results = await get_user_result(user_id)
        return results, 200
    except Exception as e:
        print(e.args)
        return jsonify(
            code=500,
            message="Unexpected error"
        ).json, 500


async def get_user_result(user_id: str):
    raw_submits = await SubmitRepository.get_student_submits(user_id)
    submits = [jsonify(
        task_name=submit.task_name,
        submit_id=submit.submit_id,
        status=result(submit.result)
    ).json for submit in raw_submits]

    return jsonify(
        user_id=user_id,
        submits=submits
    ).json


def result(r: str) -> int:
    match r:
        case "+":
            return 1
        case "-":
            return 0
        case "?":
            return 2
        case _:
            raise Exception(f"Unexpected result={r}")
