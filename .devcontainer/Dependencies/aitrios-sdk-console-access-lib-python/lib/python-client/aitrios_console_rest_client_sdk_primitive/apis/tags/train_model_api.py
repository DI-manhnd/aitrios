# coding: utf-8

"""
    AITRIOS | Console

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.1.0
    Generated by: https://openapi-generator.tech
"""

from aitrios_console_rest_client_sdk_primitive.paths.models_model_id.delete import DeleteModel
from aitrios_console_rest_client_sdk_primitive.paths.models_model_id_base.get import GetBaseModelStatus
from aitrios_console_rest_client_sdk_primitive.paths.models.get import GetModels
from aitrios_console_rest_client_sdk_primitive.paths.models.post import ImportBaseModel
from aitrios_console_rest_client_sdk_primitive.paths.models_model_id.post import PublishModel


class TrainModelApi(
    DeleteModel,
    GetBaseModelStatus,
    GetModels,
    ImportBaseModel,
    PublishModel,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass