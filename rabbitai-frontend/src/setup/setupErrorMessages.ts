import getErrorMessageComponentRegistry from 'src/components/ErrorMessage/getErrorMessageComponentRegistry';
import { ErrorTypeEnum } from 'src/components/ErrorMessage/types';
import TimeoutErrorMessage from 'src/components/ErrorMessage/TimeoutErrorMessage';
import DatabaseErrorMessage from 'src/components/ErrorMessage/DatabaseErrorMessage';
import ParameterErrorMessage from 'src/components/ErrorMessage/ParameterErrorMessage';

import setupErrorMessagesExtra from './setupErrorMessagesExtra';

/**
 * 设置错误信息，建立错误信息组件注册表并注册相关错误信息。
 */
export default function setupErrorMessages() {
  const errorMessageComponentRegistry = getErrorMessageComponentRegistry();

  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.FRONTEND_TIMEOUT_ERROR,
    TimeoutErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.BACKEND_TIMEOUT_ERROR,
    TimeoutErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.DATABASE_NOT_FOUND_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.GENERIC_DB_ENGINE_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.GENERIC_BACKEND_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.COLUMN_DOES_NOT_EXIST_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.TABLE_DOES_NOT_EXIST_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.MISSING_TEMPLATE_PARAMS_ERROR,
    ParameterErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.INVALID_TEMPLATE_PARAMS_ERROR,
    ParameterErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.RESULTS_BACKEND_NOT_CONFIGURED_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.DML_NOT_ALLOWED_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.INVALID_CTAS_QUERY_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.INVALID_CVAS_QUERY_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.QUERY_SECURITY_ACCESS_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_INVALID_HOSTNAME_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.RESULTS_BACKEND_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.ASYNC_WORKERS_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.SQLLAB_TIMEOUT_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_PORT_CLOSED_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_HOST_DOWN_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_INVALID_USERNAME_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_INVALID_PASSWORD_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_ACCESS_DENIED_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_UNKNOWN_DATABASE_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.SCHEMA_DOES_NOT_EXIST_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.OBJECT_DOES_NOT_EXIST_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.SYNTAX_ERROR,
    DatabaseErrorMessage,
  );
  errorMessageComponentRegistry.registerValue(
    ErrorTypeEnum.CONNECTION_DATABASE_PERMISSIONS_ERROR,
    DatabaseErrorMessage,
  );
  setupErrorMessagesExtra();
}
