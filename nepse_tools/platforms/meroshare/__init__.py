from decouple import config

from nepse_tools.platforms.manager import PlatformManager
from nepse_tools.utils.session import SessionManagerMixin


class MeroShare(PlatformManager, SessionManagerMixin):
    BASE_URL = "https://github.com/vaskrneup/NepseTools"

    # !! AUTH !!
    LOGIN_REQUEST_URL = "https://webbackend.cdsc.com.np/api/meroShare/auth/"
    LOGOUT_REQUEST_URL = ""
    HEADERS = {}
    # !! END AUTH !!

    # !! ADDITIONAL DATA !!
    GET_CLIENT_IDS_URL = "https://webbackend.cdsc.com.np/api/meroShare/capital/"
    # !! END ADDITIONAL DATA !!

    def __init__(self, dp: str, username: str, password: str) -> None:
        super(PlatformManager, self).__init__()
        super(SessionManagerMixin, self).__init__()

        self._dp: str = dp
        self._username: str = username
        self.__password: str = password

        # super(PlatformManager, self).__init__()

    def login(self):
        login_resp = self.post(
            self.LOGIN_REQUEST_URL,
            json={
                "clientId": self.get_client_id(),
                "username": self._username,
                "password": self.__password
            }
        )

        if login_resp.ok:
            print(login_resp.text)
        else:
            # TODO: Replace with Exception !!
            pass

    def get_client_id(self) -> int:
        data = self.get(self.GET_CLIENT_IDS_URL)

        if data.ok:
            for capital_detail in data.json():
                if capital_detail.get("code") == self._dp:
                    return int(capital_detail.get("id"))

            # TODO: Replace with Exception !!
        else:
            # TODO: Replace with Exception !!
            pass
