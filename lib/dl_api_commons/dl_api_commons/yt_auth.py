from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Optional,
)

import attr
import flask
from aiohttp import web

from dl_constants.api_constants import (
    DLCookies,
    DLHeadersCommon,
)
from dl_api_commons.base_models import AuthData

from dl_api_commons.aiohttp import aiohttp_wrappers
from dl_api_commons.base_models import TenantCommon
from dl_api_commons.flask.middlewares.commit_rci_middleware import ReqCtxInfoMiddleware


if TYPE_CHECKING:
    from aiohttp.typedefs import Handler

    from dl_api_commons.aio.typing import AIOHTTPMiddleware
    from dl_constants.api_constants import DLHeaders



class DLCookiesYT(DLCookies):
    YT_COOKIE = "YTCypressCookie"


@attr.s(frozen=True)
class YTAuthData(AuthData):
    yt_auth_cookie: str = attr.ib(repr=False)
    yt_csrf_token: str = attr.ib(repr=False)

    def get_headers(self) -> dict[DLHeaders, str]:
        return {DLHeadersCommon.CSRF_TOKEN: self.yt_csrf_token}

    def get_cookies(self) -> dict[DLCookies, str]:
        return {DLCookiesYT.YT_COOKIE: self.yt_auth_cookie}


@attr.s(frozen=True, auto_attribs=True)
class YTAuthService:
    def _before_request(self) -> None:
        temp_rci = ReqCtxInfoMiddleware.get_temp_rci().clone(
            auth_data=YTAuthData(
                yt_auth_cookie=flask.request.cookies.get(DLCookiesYT.YT_COOKIE.value),
                yt_csrf_token=flask.request.headers.get(DLHeadersCommon.CSRF_TOKEN.value)
            ),
            tenant=TenantCommon(),
        )
        temp_rci = temp_rci.clone(user_id="__fake_user_id", user_name="__fake_user_name")
        ReqCtxInfoMiddleware.replace_temp_rci(temp_rci)

    def set_up(self, app: flask.Flask) -> None:
        app.before_request(self._before_request)


def yt_auth_middleware() -> AIOHTTPMiddleware:
    @web.middleware
    @aiohttp_wrappers.DLRequestBase.use_dl_request
    async def actual_yt_auth_middleware(
        app_request: aiohttp_wrappers.DLRequestBase, handler: Handler
    ) -> web.StreamResponse:
        if aiohttp_wrappers.RequiredResourceCommon.SKIP_AUTH in app_request.required_resources:
            pass
        else:
            updated_rci = app_request.temp_rci.clone(
                auth_data=YTAuthData(
                    yt_auth_cookie=app_request.request.cookies.get(DLCookiesYT.YT_COOKIE.value),
                    yt_csrf_token=app_request.request.headers.get(DLHeadersCommon.CSRF_TOKEN.value),
                ),
                tenant=TenantCommon()
            )
            updated_rci = updated_rci.clone(user_id="__fake_user_id", user_name="__fake_user_name")
            app_request.replace_temp_rci(updated_rci)

        return await handler(app_request.request)

    return actual_yt_auth_middleware
