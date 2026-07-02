from langgraph_sdk.auth.types import StudioUser as StudioUserBase
from starlette.authentication import BaseUser

# pragma: no cover  MC8yOmFIVnBZMlhsaUpqbWxvYzZhVGhhZGc9PTo5YTMwZWRiNg==

class StudioUser(StudioUserBase, BaseUser):
    """StudioUser class."""

    def dict(self):
        return {
            "kind": "StudioUser",
            "is_authenticated": self.is_authenticated,
            "display_name": self.display_name,
            "identity": self.identity,
            "permissions": self.permissions,
        }
# pylint: disable  MS8yOmFIVnBZMlhsaUpqbWxvYzZhVGhhZGc9PTo5YTMwZWRiNg==
