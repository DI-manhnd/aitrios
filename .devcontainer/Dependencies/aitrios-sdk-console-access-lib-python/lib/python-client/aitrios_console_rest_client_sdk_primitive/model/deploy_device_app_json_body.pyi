# coding: utf-8

"""
    AITRIOS | Console

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.1.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from aitrios_console_rest_client_sdk_primitive import schemas  # noqa: F401


class DeployDeviceAppJsonBody(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    DeployDeviceApp Json Body
    """


    class MetaOapg:
        required = {
            "app_name",
            "version_number",
            "device_ids",
        }
        
        class properties:
            app_name = schemas.StrSchema
            version_number = schemas.StrSchema
            device_ids = schemas.StrSchema
            deploy_parameter = schemas.StrSchema
            comment = schemas.StrSchema
            __annotations__ = {
                "app_name": app_name,
                "version_number": version_number,
                "device_ids": device_ids,
                "deploy_parameter": deploy_parameter,
                "comment": comment,
            }
    
    app_name: MetaOapg.properties.app_name
    version_number: MetaOapg.properties.version_number
    device_ids: MetaOapg.properties.device_ids
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["app_name"]) -> MetaOapg.properties.app_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["version_number"]) -> MetaOapg.properties.version_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["device_ids"]) -> MetaOapg.properties.device_ids: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deploy_parameter"]) -> MetaOapg.properties.deploy_parameter: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["comment"]) -> MetaOapg.properties.comment: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["app_name", "version_number", "device_ids", "deploy_parameter", "comment", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["app_name"]) -> MetaOapg.properties.app_name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["version_number"]) -> MetaOapg.properties.version_number: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["device_ids"]) -> MetaOapg.properties.device_ids: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deploy_parameter"]) -> typing.Union[MetaOapg.properties.deploy_parameter, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["comment"]) -> typing.Union[MetaOapg.properties.comment, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["app_name", "version_number", "device_ids", "deploy_parameter", "comment", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        app_name: typing.Union[MetaOapg.properties.app_name, str, ],
        version_number: typing.Union[MetaOapg.properties.version_number, str, ],
        device_ids: typing.Union[MetaOapg.properties.device_ids, str, ],
        deploy_parameter: typing.Union[MetaOapg.properties.deploy_parameter, str, schemas.Unset] = schemas.unset,
        comment: typing.Union[MetaOapg.properties.comment, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DeployDeviceAppJsonBody':
        return super().__new__(
            cls,
            *args,
            app_name=app_name,
            version_number=version_number,
            device_ids=device_ids,
            deploy_parameter=deploy_parameter,
            comment=comment,
            _configuration=_configuration,
            **kwargs,
        )
