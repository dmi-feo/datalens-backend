import marshmallow as ma

from dl_file_uploader_api_lib.schemas.base import BaseRequestSchema


class CleanupRequestSchema(BaseRequestSchema):
    tenant_id = ma.fields.String(required=True)


class RenameFilesRequestSchema(BaseRequestSchema):
    old_tenant_id = ma.fields.String(allow_none=True, load_default=None)
    tenant_id = ma.fields.String(required=True)
