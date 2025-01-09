import logging
from datetime import timedelta

from shared.config import get_config
from shared.storage.minio import MinioStorageService

log = logging.getLogger(__name__)


MINIO_CLIENT = None


# Service class for interfacing with codecov's underlying storage layer, minio
class StorageService(MinioStorageService):
    def __init__(self, in_config=None):
        global MINIO_CLIENT  # noqa: PLW0603

        # init minio
        if in_config is None:
            self.minio_config = get_config("services", "minio", default={})
            log.info("DEBUG_BUNDLE: in_config is none, read config", extra=dict(minio_config=self.minio_config))
        else:
            self.minio_config = in_config
            log.info("DEBUG_BUNDLE: set config from in_config", extra=dict(minio_config=self.minio_config))

        if "host" not in self.minio_config:
            self.minio_config["host"] = "minio"
        if "port" not in self.minio_config:
            self.minio_config["port"] = 9000
        if "iam_auth" not in self.minio_config:
            self.minio_config["iam_auth"] = False
        if "iam_endpoint" not in self.minio_config:
            self.minio_config["iam_endpoint"] = None

        log.info("DEBUG_BUNDLE: updated config with default value", extra=dict(minio_config=self.minio_config))

        if not MINIO_CLIENT:
            MINIO_CLIENT = self.init_minio_client(
                self.minio_config["host"],
                self.minio_config["port"],
                self.minio_config["access_key_id"],
                self.minio_config["secret_access_key"],
                self.minio_config["verify_ssl"],
                self.minio_config["iam_auth"],
                self.minio_config["iam_endpoint"],
            )
            log.info("----- created minio_client: ---- ")
        self.minio_client = MINIO_CLIENT

    def create_presigned_put(self, bucket, path, expires):
        expires = timedelta(seconds=expires)
        log.info("DEBUG_BUNDLE: create_presigned_put", extra=dict(bucket=bucket,path=path))
        return self.minio_client.presigned_put_object(bucket, path, expires)

    def create_presigned_get(self, bucket, path, expires):
        expires = timedelta(seconds=expires)
        log.info("DEBUG_BUNDLE: create_presigned_get", extra=dict(bucket=bucket,path=path))
        return self.minio_client.presigned_get_object(bucket, path, expires)
