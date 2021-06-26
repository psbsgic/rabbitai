
import getErrorMessageComponentRegistry from 'src/components/ErrorMessage/getErrorMessageComponentRegistry';
import { ErrorTypeEnum } from 'src/components/ErrorMessage/types';
import TimeoutErrorMessage from 'src/components/ErrorMessage/TimeoutErrorMessage';
import DatabaseErrorMessage from 'src/components/ErrorMessage/DatabaseErrorMessage';
import ParameterErrorMessage from 'src/components/ErrorMessage/ParameterErrorMessage';

import setupErrorMessagesExtra from './setupErrorMessagesExtra';

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
    ErrorTypeEnum.GENERIC_DB_ENGINE_ERROR,
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
    ErrorTypeEnum.CONNECTION_INVALID_HOSTNAME_ERROR,
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
    ErrorTypeEnum.CONNECTION_DATABASE_PERMISSIONS_ERROR,
    DatabaseErrorMessage,
  );
  setupErrorMessagesExtra();
}
