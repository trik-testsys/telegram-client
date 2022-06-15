import json
from typing import List

from bot.model.Submit import Submit
from bot.repository.SubmitRepository import SubmitRepository
from bot.repository.UserRepository import UserRepository
from bot.service.GradingService import GradingService
from bot.teletrik.DI import service


@service
class LektoriumService:
    def __init__(
        self,
        submit_repository: SubmitRepository,
        user_repository: UserRepository,
        grading_service: GradingService,
    ):
        self.submit_repository: SubmitRepository = submit_repository
        self.user_repository: UserRepository = user_repository
        self.grading_service: GradingService = grading_service

    NO_POSITIVE_SUBMIT = 0
    GRADING_ERROR = 1

    async def get_task_info(self, task_name: str, user_id: str):
        submit_id: str | None = await self._get_positive_submit_id(task_name, user_id)
        if submit_id is None:
            return self.NO_POSITIVE_SUBMIT
        result = await self.grading_service.get_lektorium_info(submit_id)
        if result == self.grading_service.SERVER_ERROR:
            return self.GRADING_ERROR
        return json.loads(result)

    async def _get_positive_submit_id(self, task_name: str, user_id: str) -> str | None:
        submits: List[
            Submit
        ] = await self.submit_repository.get_student_submits_by_task(user_id, task_name)
        for submit in submits:
            if submit.result == "+":
                return submit.submit_id

        return None
