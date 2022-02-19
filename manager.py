from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare

ms = MeroShare(
    dp=config("MEROSHARE_DP"),
    username=config("MEROSHARE_USERNAME"),
    password=config("MEROSHARE_PASSWORD")
)
ms.login()

# _vars = vars(ms)

# for k, v in _vars.items():
#     if type(v) is list:
#         for d in v:
#             print(d)
#     else:
#         print(k, "::", v)
