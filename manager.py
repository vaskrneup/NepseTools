from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare

ms = MeroShare(
    dp=config("MEROSHARE_DP"),
    username=config("MEROSHARE_USERNAME"),
    password=config("MEROSHARE_PASSWORD")
)
ms.login()
