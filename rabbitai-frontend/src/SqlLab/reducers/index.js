
import { combineReducers } from 'redux';

import sqlLab from './sqlLab';
import localStorageUsageInKilobytes from './localStorageUsage';
import messageToasts from '../../messageToasts/reducers/index';
import common from './common';

export default combineReducers({
  sqlLab,
  localStorageUsageInKilobytes,
  messageToasts,
  common,
});
